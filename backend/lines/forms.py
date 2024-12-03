import datetime as dt
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Counters

class ReadDataCounters(forms.Form):
    day = forms.DateField(initial=dt.date.today)
    # department = forms.CharField(max_length=255)
