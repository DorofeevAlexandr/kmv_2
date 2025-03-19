import datetime as dt


from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from .forms import (ReadDataCounters, ReadAndSaveLinesStatistic)
from .work_with_data import (get_data_in_select_date, get_departments, get_departments_ppk,
                             get_lines_from_base, get_sorted_departments_data, get_sorted_departments_statistic,
                             get_statistics_select_period, change_speed_lines)
from .models import Lines, LinesCurrentParams

menu = [{'title': "Данные за день", 'url_name': 'home'},
        {'title': "Статистика за месяц", 'url_name': 'statistic'},
        # {'title': "Статистика за год", 'url_name': 'statistics_for_the_year'},
        {'title': "", 'url_name': 'tuning'},
]

menu_ppk = [{'title': "Данные за день ППК", 'url_name': 'data_in_day_ppk'},
        {'title': "Статистика за месяц ППК", 'url_name': 'statistic_ppk'},
        # {'title': "Статистика за год ППК", 'url_name': 'statistics_for_the_year_ppk'},
        {'title': "", 'url_name': 'tuning'},
]


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


def data_in_day_ppk(request):
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

    departments = get_departments_ppk(lines)
    out_department = get_sorted_departments_data(departments, lines_statistic, smale_speed_lines)

    data = {
        'title': 'КМВ - Данные за день ППК',
        'departments': out_department,
        'form': form,
        'times': time,
        'menu': menu_ppk,
    }
    return render(request, 'lines/index.html', context=data)


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


def statistic_ppk(request):
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

    departments = get_departments_ppk(lines)
    out_department = get_sorted_departments_statistic(departments, made_kabel_in_days)

    data = {
        'title': 'КМВ - Статистика за месяц ППК',
        'menu': menu_ppk,
        'departments': out_department,
        'form': form,
        'times': times,
    }
    return render(request, 'lines/statistic.html', context=data)


def statistics_for_the_year(request):
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
        'title': 'КМВ - Статистика за год',
        'menu': menu,
        'departments': out_department,
        'form': form,
        'times': times,
    }
    return render(request, 'lines/statistics_for_the_year.html', context=data)


def statistics_for_the_year_ppk(request):
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

    departments = get_departments_ppk(lines)
    out_department = get_sorted_departments_statistic(departments, made_kabel_in_days)

    data = {
        'title': 'КМВ - Статистика за год ППК',
        'menu': menu_ppk,
        'departments': out_department,
        'form': form,
        'times': times,
    }
    return render(request, 'lines/statistics_for_the_year.html', context=data)


def get_lines_params_from_base():
    out_lines = []
    lines = Lines.objects.order_by('line_number')
    # lines_current_params = LinesCurrentParams.objects.order_by('id')
    # print(*lines_current_params)
    # filds = LinesCurrentParams._meta
    for line in lines:
        # print(line)
        line_number = line.line_number
        # print(line_number)
        # line_current_params = filter(lambda l: l.line_number==line_number, lines_current_params)
        line_current_params = LinesCurrentParams.objects.get(line_number=int(line_number))
        # print(line_current_params.__repr__())
        out_lines.append({'line_number': line.line_number,
                            'name': line.name,
                            'modbus_adr': line.modbus_adr,
                            'pseudonym': line.pseudonym ,
                            'port': line.port,
                            'department': line.department,
                            'number_of_display': line.number_of_display,
                            'k': line.k,
                            'indicator_value': line_current_params.indicator_value,
                            'length': line_current_params.length,
                            'speed_line': line_current_params.speed_line,
                          })
    return  out_lines


def tuning(request):
    lines = get_lines_params_from_base()
    data = {
        'title': 'КМВ - настройка',
        'menu': menu,
        'lines': lines,
    }
    return render(request, 'lines/tuning.html', context=data)


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
