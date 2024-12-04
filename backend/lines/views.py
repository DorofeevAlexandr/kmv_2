import datetime as dt
from os import times

from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from .forms import ReadDataCounters, get_counters_values_from_base, get_speed_lines, get_lines_statistic, get_lines_from_base

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Цех №1", 'url_name': 'index'},
        {'title': "Цех №2", 'url_name': 'index'},
        {'title': "Цех №3", 'url_name': 'index'}
]


def index(request):
    speed_lines = []
    lines_statistic = []
    time = []
    lines = get_lines_from_base()
    if request.method == 'POST':
        form = ReadDataCounters(request.POST, request.FILES)
        if form.is_valid():
            select_date = form.cleaned_data.get('day', None)
            print(select_date)
            if select_date:

                counters_values = get_counters_values_from_base(select_date)
                speed_lines = get_speed_lines(counters_values)
                time = [dt.timedelta(minutes=n) for n, speed in enumerate(speed_lines)]
                lines_statistic = get_lines_statistic(speed_lines)

    else:
        form = ReadDataCounters()

    out_lines = []
    for line in lines:
        n = line['line_number']
        if lines_statistic and speed_lines:
            out_lines.append({**line,
                              'statistic': lines_statistic[n],
                              'speed': speed_lines[n]} )
    data = {
        'title': 'КМВ',
        #'menu': menu,
        'lines': out_lines,
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

