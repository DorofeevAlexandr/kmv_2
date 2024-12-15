import datetime as dt
from os import times

from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from .forms import (ReadDataCounters, get_counters_values_from_base, get_speed_lines, get_lines_statistic,
                    get_lines_from_base, antialiasing_speed_value)

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Цех №1", 'url_name': 'index'},
        {'title': "Цех №2", 'url_name': 'index'},
        {'title': "Цех №3", 'url_name': 'index'}
]


def get_smale_speed_lines(speed_lines: list):
    result = []
    for num_lines in range(len(speed_lines)):
        result.append([])
        for minute in range(0, len(speed_lines[num_lines]), 5):
            result[num_lines].append(speed_lines[num_lines][minute])
    return result


def index(request):
    smale_speed_lines = []
    lines_statistic = []
    time = []
    lines = get_lines_from_base()
    if request.method == 'POST':
        form = ReadDataCounters(request.POST, request.FILES)
        if form.is_valid():
            select_date = form.cleaned_data.get('day', None)
            # print(select_date)
            if select_date:

                counters_values = get_counters_values_from_base(select_date)
                # print(counters_values)
                speed_lines = get_speed_lines(counters_values)
                antialiasing_speed_value(speed_lines)
                # print(speed_lines)

                lines_statistic = get_lines_statistic(speed_lines)
                smale_speed_lines = get_smale_speed_lines(speed_lines)
                time = [dt.time(hour=(((n * 5) // 60) + 8) % 24, minute=((n * 5) % 60)) for n, speed in
                        enumerate(smale_speed_lines[0])]

    else:
        form = ReadDataCounters()
    print(dt.datetime.now())
    department_1 = sorted(filter(lambda line: line['department'] == '1', lines), key=lambda l: l["number_of_display"])
    department_2 = sorted(filter(lambda line: line['department'] == '2', lines), key=lambda l: l["number_of_display"])
    department_3 = sorted(filter(lambda line: line['department'] == '3', lines), key=lambda l: l["number_of_display"])
    department_4 = sorted(filter(lambda line: line['department'] == 'ППК', lines), key=lambda l: l["number_of_display"])
    departments = [
        department_1,
        department_2,
        department_3,
        department_4
    ]

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
    data = {
        'title': 'КМВ',
        #'menu': menu,
        'departments': out_department,
        'form': form,
        'times': time,
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

