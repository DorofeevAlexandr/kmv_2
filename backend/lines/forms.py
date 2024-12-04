import datetime as dt
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible
from django.db import models

from .models import Counters

class ReadDataCounters(forms.Form):
    day = forms.DateField(initial=dt.date.today)
    # department = forms.CharField(max_length=255)


def get_counters_values_from_base(date: dt.date):
    dtime_8_hours = dt.timedelta(hours=8)
    dtime_1_days = dt.timedelta(days=1)
    time_start = dt.datetime(year=date.year,
                             month=date.month,
                             day=date.day,
                             hour=0,
                             minute=0,
                             second=0) + dtime_8_hours
    time_end = time_start + dtime_1_days
    counters = Counters.objects.filter(time__range=[time_start, time_end]).order_by('-time')

    length_in_minute = [[] for _ in range(1441)]

    for c in counters:
        minutes = (c.time - time_start).seconds // 60
        length_in_minute[minutes] = c.lengths
    return  length_in_minute


def get_speed_lines(length_in_minute):
    speed_lines = [[[] for _ in range(1441)] for _ in range(100)]

    for n_minute in range(1, 1441):
        length_lines = length_in_minute[n_minute]
        for n_line, length in enumerate(length_lines):
            try:
                speed_lines[n_line][n_minute] = (length_in_minute[n_minute][n_line] -
                                                 length_in_minute[n_minute - 1][n_line] / 1000)
                if speed_lines[n_line][n_minute] > 10000:
                    speed_lines[n_line][n_minute] = 0
            except:
                speed_lines[n_line][n_minute] = 0

    # for line in speed_lines:
    #     print('--------------------')
    #     print(line)

    return speed_lines


