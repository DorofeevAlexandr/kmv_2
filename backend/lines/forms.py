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
                          max_value = dt.date.today().year,
                          min_value = 2024,
                          step_size = 1,
                          )


class LineParamsKUpdateForm(forms.Form):
    # line_number = forms.IntegerField(required=True,
    #                                  min_value=1,
    #                                  max_value=255)
    # name =  forms.CharField(max_length=255,
    #                         label="Название линии",
    #                         required=True,
    #                         widget=forms.TextInput(attrs={'class': 'form-input'}),
    #                         )
    # pseudonym =  forms.CharField(max_length=255,
    #                         label="Название линии",
    #                         required=True,
    #                         widget=forms.TextInput(attrs={'class': 'form-input'}),
    #                         )
    # port =  forms.CharField(max_length=255,
    #                         label="Порт",
    #                         required=True,
    #                         widget=forms.TextInput(attrs={'class': 'form-input'}),
    #                         )
    # modbus_adr = forms.IntegerField(required=True,
    #                                  min_value=1,
    #                                  max_value=255)
    # department = forms.IntegerField(required=True,
    #                                  min_value=1,
    #                                  max_value=255)
    # number_of_display = forms.IntegerField(required=True,
    #                                  min_value=0,
    #                                  max_value=255)
    # cable_number = forms.IntegerField(required=True,
    #                                  min_value=0,
    #                                  max_value=255)
    # cable_connection_number = forms.IntegerField(required=True,
    #                                  min_value=0,
    #                                  max_value=255)
    k = forms.FloatField(required=True,
                         min_value=0,
                         step_size=0.000000000000000001,
                         )
    # created_dt = forms.DateTimeField(blank=True, null=True)
    # description = forms.CharField(blank=True, null=True)
