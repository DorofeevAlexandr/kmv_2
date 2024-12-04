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

    length_in_minute = [[] for _ in range(1440)]

    for c in counters:
        minutes = (c.time - time_start).seconds // 60
        length_in_minute[minutes] = c.lengths
    return  length_in_minute


