import datetime as dt
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible
from django.db import models


class ReadDataCounters(forms.Form):
    day = forms.DateField(initial=dt.date.today,
                          label="Выберите дату",
                          required=True,
                          widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
                          input_formats=["%Y-%m-%d"]
                          )


class ReadAndSaveLinesStatistic(forms.Form):
    start_day = forms.DateField(initial=dt.date.today,
                          label="Выберите месяц",
                          required=True,
                          widget=forms.DateInput(format="%Y-%m", attrs={"type": "month"}),
                          input_formats=["%Y-%m"]
                          )


class SelectYearLinesStatistic(forms.Form):
    select_year = forms.IntegerField(initial=dt.date.today().year,
                          label="Выберите год",
                          required=True,
                          max_value = dt.date.today().year+1,
                          min_value = 2024,
                          step_size = 1,
                          )


#
# class LineParamsUpdate(forms.Form):
#     line_number = forms.IntegerField(unique=True)
#     name = forms.CharField(unique=True, max_length=1)
#     pseudonym = forms.CharField(unique=True, max_length=1)
#     port = forms.CharField(max_length=1)
#     modbus_adr = forms.IntegerField()
#     department = forms.IntegerField()
#     number_of_display = forms.IntegerField()
#     cable_number = forms.IntegerField()
#     cable_connection_number = forms.IntegerField()
#     k = forms.FloatField()
#     created_dt = forms.DateTimeField(blank=True, null=True)
#     description = forms.CharField(blank=True, null=True)