import datetime as dt
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible
from django.db import models

from .models import Counters, Lines


COUNT_LINES = 70

class ReadDataCounters(forms.Form):
    day = forms.DateField(initial=dt.date.today,
                          label="Выберите дату",
                          required=True,
                          widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
                          input_formats=["%Y-%m-%d"]
                          )

    # department = forms.CharField(max_length=255)

def get_lines_from_base():
    out_lines = []
    lines = Lines.objects.order_by('department')
    for l in lines:
        out_lines.append({'line_number': l.line_number,
                            'name': l.name,
                            'pseudonym': l.pseudonym ,
                            'port': l.port,
                            'department': l.department,
                            'number_of_display': l.number_of_display,
                          })
    return  out_lines

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
    speed_lines = [[0 for _ in range(1441)] for _ in range(COUNT_LINES)]

    for n_minute in range(1, 1441):
        length_lines = length_in_minute[n_minute]
        for n_line, length in enumerate(length_lines):
            try:
                speed = (length_in_minute[n_minute][n_line] -
                        length_in_minute[n_minute - 1][n_line]) / 1000
                if speed > 10000 or speed < 0:
                    speed_lines[n_line][n_minute] = 0
                else:
                    speed_lines[n_line][n_minute] = speed
            except:
                speed_lines[n_line][n_minute] = 0

    # for line in speed_lines:
    #     print('--------------------')
    #     print(line)
    return speed_lines

def num_smena(minute):
    hour = minute // 60
    if 0 <= hour < 12:
        return 1
    else:
        return 2


def antialiasing_speed_value(speed_lines: list):
    for num_lines in range(len(speed_lines)):
        speed0 = speed_lines[num_lines][0]
        speed1 = speed_lines[num_lines][1]
        speed2 = speed_lines[num_lines][2]
        average_speed = (speed0 + speed1 + speed2) / 3
        speed_lines[num_lines][0] = average_speed
        speed_lines[num_lines][1] = average_speed
        for minute in range(len(speed_lines[num_lines])):
            speed2 = speed_lines[num_lines][minute]
            average_speed = (speed0 + speed1 + speed2) / 3
            speed_lines[num_lines][minute] = average_speed
            speed0 = speed1
            speed1 = speed2


def get_str_time(minutes: int):
    hour = minutes // 60
    minute = minutes % 60
    return dt.time(hour=hour, minute=minute).strftime('%H:%M')


def str_average_speed(made_kabel: float, minutes: int):
    if minutes == 0:
        average_speed = 0
    else:
        average_speed = made_kabel / minutes

    return f"{average_speed:5.1f}"


def get_lines_statistic(speed_lines):
    lines_statistic = []

    for num_line in range(COUNT_LINES):
        line_runing = False
        line_statistic = {
            'count_minute_line_run': 0,
            'count_minute_line_run_1': 0,
            'count_minute_line_run_2': 0,

            'max_value': 0,
            'max_value_1': 0,
            'max_value_2': 0,

            'made_kabel': 0,
            'made_kabel_1': 0,
            'made_kabel_2': 0,

            'stop_count': 0,
            'stop_count_1': 0,
            'stop_count_2': 0,
        }

        for minute in range(1438):
            metr_in_minute = speed_lines[num_line][minute]
            metr_in_minute = float(metr_in_minute)
            smena = num_smena(minute)

            if metr_in_minute > 0.2:
                line_runing = True
                line_statistic['count_minute_line_run'] += 1
                if smena == 1:
                    line_statistic['count_minute_line_run_1'] += 1
                if smena == 2:
                    line_statistic['count_minute_line_run_2'] += + 1
            else:
                if line_runing:
                    line_statistic['stop_count'] += 1
                    if smena == 1:
                        line_statistic['stop_count_1'] += 1
                    if smena == 2:
                        line_statistic['stop_count_2'] += 1
                    line_runing = False


            line_statistic['max_value'] = max(line_statistic['max_value'], metr_in_minute)
            if smena == 1:
                line_statistic['max_value_1'] = max(line_statistic['max_value_1'], metr_in_minute)
            if smena == 2:
                line_statistic['max_value_2'] = max(line_statistic['max_value_2'], metr_in_minute)

            line_statistic['made_kabel'] += metr_in_minute
            if smena == 1:
                line_statistic['made_kabel_1'] += metr_in_minute
            if smena == 2:
                line_statistic['made_kabel_2'] += metr_in_minute

        line_statistic['average_speed'] = str_average_speed(line_statistic['made_kabel'], line_statistic['count_minute_line_run'])
        line_statistic['average_speed_1'] = str_average_speed(line_statistic['made_kabel_1'], line_statistic['count_minute_line_run_1'])
        line_statistic['average_speed_2'] = str_average_speed(line_statistic['made_kabel_2'], line_statistic['count_minute_line_run_2'])

        line_statistic['made_kabel'] = line_statistic['made_kabel'] / 1000
        line_statistic['made_kabel_1'] = line_statistic['made_kabel_1'] / 1000
        line_statistic['made_kabel_2'] = line_statistic['made_kabel_2'] / 1000

        line_statistic['count_minute_line_run'] = get_str_time(line_statistic['count_minute_line_run'])
        line_statistic['count_minute_line_run_1'] = get_str_time(line_statistic['count_minute_line_run_1'])
        line_statistic['count_minute_line_run_2'] = get_str_time(line_statistic['count_minute_line_run_2'])

        line_statistic['max_value'] = f"{line_statistic['max_value']:5.1f}"
        line_statistic['max_value_1'] = f"{line_statistic['max_value_1']:5.1f}"
        line_statistic['max_value_2'] = f"{line_statistic['max_value_2']:5.1f}"

        line_statistic['made_kabel'] = f"{line_statistic['made_kabel']:5.1f}"
        line_statistic['made_kabel_1'] = f"{line_statistic['made_kabel_1']:5.1f}"
        line_statistic['made_kabel_2'] = f"{line_statistic['made_kabel_2']:5.1f}"

        lines_statistic.append(line_statistic)

    return lines_statistic
