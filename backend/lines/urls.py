from django.urls import path, re_path, register_converter
from . import views
from . import converters


register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.index, name='home'),
    path('statistic', views.statistic, name='statistic'),
    path('ppk', views.index, name='home_ppk'),
    path('statistic_ppk', views.statistic, name='statistic_ppk'),
    path('tuning', views.tuning, name='tuning'),
]
