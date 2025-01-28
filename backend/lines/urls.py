from django.urls import path, re_path, register_converter
from . import views
from . import converters


register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.index, name='home'),
    path('statistic', views.statistic, name='statistic'),
    path('ppk', views.data_in_day_ppk, name='data_in_day_ppk'),
    path('statistic_ppk', views.statistic_ppk, name='statistic_ppk'),
    path('tuning', views.tuning, name='tuning'),
]
