import datetime as dt
from calendar import month, Month
from os import times
from dateutil.relativedelta import relativedelta

from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from .forms import (ReadDataCounters, ReadAndSaveLinesStatistic, get_counters_values_from_base, get_speed_lines, get_lines_statistic,
                    get_lines_from_base, antialiasing_speed_value, change_lines_statistic, change_speed_lines)

menu = [{'title': "Данные за день", 'url_name': 'home'},
        {'title': "Статистика за месяц", 'url_name': 'statistic'},
        {'title': "", 'url_name': 'tuning'},
]

menu_ppk = [{'title': "Данные за день ППК", 'url_name': 'home_ppk'},
        {'title': "Статистика за месяц ППК", 'url_name': 'statistic_ppk'},
        {'title': "", 'url_name': 'tuning'},
]


def get_smale_speed_lines(speed_lines: list):
    result = []
    for num_lines in range(len(speed_lines)):
        result.append([])
        for minute in range(0, len(speed_lines[num_lines]), 5):
            result[num_lines].append(speed_lines[num_lines][minute])
    return result


def get_departments(lines: list):
    department_1 = sorted(filter(lambda line: line['department'] == '1', lines), key=lambda l: l["number_of_display"])
    department_2 = sorted(filter(lambda line: line['department'] == '2', lines), key=lambda l: l["number_of_display"])
    department_3 = sorted(filter(lambda line: line['department'] == '3', lines), key=lambda l: l["number_of_display"])
    # department_4 = sorted(filter(lambda line: line['department'] == 'ППК', lines), key=lambda l: l["number_of_display"])
    return [
            department_1,
            department_2,
            department_3,
            # department_4
           ]


def get_data_in_select_date(select_date: dt.datetime):
    counters_values = get_counters_values_from_base(select_date)
    # print(counters_values)
    speed_lines = get_speed_lines(counters_values)
    antialiasing_speed_value(speed_lines)
    # print(speed_lines)

    lines_statistic = get_lines_statistic(speed_lines)
    change_lines_statistic(lines_statistic)
    smale_speed_lines = get_smale_speed_lines(speed_lines)
    change_speed_lines(smale_speed_lines)
    time = [dt.time(hour=(((n * 5) // 60) + 8) % 24, minute=((n * 5) % 60)) for n, speed in
            enumerate(smale_speed_lines[0])]
    return time, smale_speed_lines, lines_statistic


def get_sorted_departments_data(departments, lines_statistic, smale_speed_lines):
    out_department = []
    for department in departments:
        out_lines = []
        for line in department:
            n = line['line_number']
            if lines_statistic and smale_speed_lines:
                speed = [int(sp) for sp in  smale_speed_lines[n - 1]]
                out_lines.append({**line,
                                  'statistic': lines_statistic[n - 1],
                                  'speed': speed} )
        out_department.append(out_lines)
    return out_department


def index(request):
    smale_speed_lines = []
    lines_statistic = []
    time = []
    lines = get_lines_from_base()
    if request.method == 'POST':
        form = ReadDataCounters(request.POST, request.FILES)
        if form.is_valid():
            select_date = form.cleaned_data.get('day', None)
            if select_date:
                time, smale_speed_lines, lines_statistic = get_data_in_select_date(select_date)
    else:
        form = ReadDataCounters()

    departments = get_departments(lines)
    out_department = get_sorted_departments_data(departments, lines_statistic, smale_speed_lines)

    data = {
        'title': 'КМВ - Данные за день',
        'departments': out_department,
        'form': form,
        'times': time,
        'menu': menu,
    }
    return render(request, 'lines/index.html', context=data)


def get_statistics_select_period(start_date: dt.date):
    end_date = start_date + relativedelta(months=1)

    made_kabel_in_days = []
    times = []

    if start_date:
        cur_date = start_date
        made_kabel_in_days = []
        times = []
        while cur_date < end_date:
            # print(cur_date)
            counters_values = get_counters_values_from_base(cur_date)
            speed_lines = get_speed_lines(counters_values)
            antialiasing_speed_value(speed_lines)
            lines_statistic = get_lines_statistic(speed_lines)
            made_kabel_in_days.append([int(float(ls['made_kabel'])) for ls in lines_statistic])
            times.append(cur_date)

            cur_date = cur_date + dt.timedelta(days=1)
        # print(made_kabel_in_days)
    return times, made_kabel_in_days


def get_sorted_departments_statistic(departments, made_kabel_in_days):
    out_department = []
    for department in departments:
        out_lines = []
        for line in department:
            n = line['line_number']
            if made_kabel_in_days:
                made_kabel = [day_values[n - 1] for day_values in  made_kabel_in_days]
                out_lines.append({**line,
                                  'sum_made_kabel': sum(made_kabel),
                                  'made_kabel': made_kabel} )
        out_department.append(out_lines)
    return out_department

def statistic(request):
    made_kabel_in_days = []
    times = []
    lines = get_lines_from_base()
    if request.method == 'POST':
        form = ReadAndSaveLinesStatistic(request.POST, request.FILES)
        if form.is_valid():
            calendar_date = form.cleaned_data.get('start_day', None)
            start_date = dt.date(year=calendar_date.year,
                                 month=calendar_date.month,
                                 day=1)
            times, made_kabel_in_days = get_statistics_select_period(start_date)
    else:
        form = ReadAndSaveLinesStatistic()

    departments = get_departments(lines)
    out_department = get_sorted_departments_statistic(departments, made_kabel_in_days)

    data = {
        'title': 'КМВ - Статистика за месяц',
        'menu': menu,
        'departments': out_department,
        'form': form,
        'times': times,
    }
    return render(request, 'lines/statistic.html', context=data)



def tuning(request):

    data = {
        'title': 'КМВ',
         'menu': menu,
    }
    return render(request, 'lines/index.html', context=data)



def about(request):
    return render(request, 'lines/about.html')


def categories(request, cat_id):
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>id: {cat_id}</p>")


def categories_by_slug(request, cat_slug):
    if request.POST:
        print(request.POST)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>slug: {cat_slug}</p>")


def archive(request, year):
    if year > 2023:
        uri = reverse('cats', args=('sport', ))
        return HttpResponsePermanentRedirect(uri)

    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

