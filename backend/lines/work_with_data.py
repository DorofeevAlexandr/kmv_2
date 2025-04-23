import datetime as dt
from django.shortcuts import get_object_or_404
from calendar import month, Month
from os import times
from dateutil.relativedelta import relativedelta
import operator
from .models import Counters, Lines, LinesStatistics


COUNT_LINES = 70


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

    return f"{average_speed:6.1f}"


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

        line_statistic['kmv'] = f"{(line_statistic['count_minute_line_run'] / 1440 * 100.0) :6.1f}"
        line_statistic['kmv_1'] = f"{(line_statistic['count_minute_line_run_1'] / 720 * 100.0) :6.1f}"
        line_statistic['kmv_2'] = f"{(line_statistic['count_minute_line_run_2'] / 720 * 100.0) :6.1f}"

        line_statistic['average_speed'] = str_average_speed(line_statistic['made_kabel'], line_statistic['count_minute_line_run'])
        line_statistic['average_speed_1'] = str_average_speed(line_statistic['made_kabel_1'], line_statistic['count_minute_line_run_1'])
        line_statistic['average_speed_2'] = str_average_speed(line_statistic['made_kabel_2'], line_statistic['count_minute_line_run_2'])

        line_statistic['made_kabel'] = line_statistic['made_kabel'] / 1000
        line_statistic['made_kabel_1'] = line_statistic['made_kabel_1'] / 1000
        line_statistic['made_kabel_2'] = line_statistic['made_kabel_2'] / 1000

        line_statistic['count_minute_line_run'] = get_str_time(line_statistic['count_minute_line_run'])
        line_statistic['count_minute_line_run_1'] = get_str_time(line_statistic['count_minute_line_run_1'])
        line_statistic['count_minute_line_run_2'] = get_str_time(line_statistic['count_minute_line_run_2'])

        line_statistic['max_value'] = f"{line_statistic['max_value']:6.1f}"
        line_statistic['max_value_1'] = f"{line_statistic['max_value_1']:6.1f}"
        line_statistic['max_value_2'] = f"{line_statistic['max_value_2']:6.1f}"

        line_statistic['made_kabel'] = f"{line_statistic['made_kabel']:6.1f}"
        line_statistic['made_kabel_1'] = f"{line_statistic['made_kabel_1']:6.1f}"
        line_statistic['made_kabel_2'] = f"{line_statistic['made_kabel_2']:6.1f}"

        line_statistic['label_count_minute_line_run'] = 'Время работы'
        line_statistic['label_max_value'] = 'Макс. скорость, м/мин	'
        line_statistic['label_average_speed'] = 'Средн. скорость, м/мин	'
        line_statistic['label_made_kabel'] = 'Изготовленно, км'
        line_statistic['label_stop_count'] = 'Количество остановок'
        line_statistic['label_kmv'] = 'КМВ'


        lines_statistic.append(line_statistic)

    return lines_statistic


def change_line_stat_twists_in_minute(lines_statistic: list, n: int):
    lines_statistic[n - 1]['label_max_value'] = 'Макс. скорость, скруток/мин'
    lines_statistic[n - 1]['label_average_speed'] = 'Средн. скорость, скруток/мин'
    lines_statistic[n - 1]['label_made_kabel'] = 'Изготовленно, тыс. скруток'


def change_line_stat_kg_in_minute(lines_statistic: list, n: int):
    lines_statistic[n - 1]['label_max_value'] = 'Макс. скорость, кг/мин'
    lines_statistic[n - 1]['label_average_speed'] = 'Средн. скорость, кг/мин'
    lines_statistic[n - 1]['label_made_kabel'] = 'Изготовленно, т.'


def change_line_stat_metr_in_second(lines_statistic: list, n: int):
    lines_statistic[n - 1]['label_max_value'] = 'Макс. скорость, м/с'
    lines_statistic[n - 1]['label_average_speed'] = 'Средн. скорость, м/с'

    lines_statistic[n - 1]['max_value'] = f"{(float(lines_statistic[n - 1]['max_value']) / 60.0):5.1f}"
    lines_statistic[n - 1]['max_value_1'] = f"{(float(lines_statistic[n - 1]['max_value_1']) / 60.0):5.1f}"
    lines_statistic[n - 1]['max_value_2'] = f"{(float(lines_statistic[n - 1]['max_value_2']) / 60.0):5.1f}"

    lines_statistic[n - 1]['average_speed'] = f"{(float(lines_statistic[n - 1]['average_speed']) / 60.0):5.1f}"
    lines_statistic[n - 1]['average_speed_1'] = f"{(float(lines_statistic[n - 1]['average_speed_1']) / 60.0):5.1f}"
    lines_statistic[n - 1]['average_speed_2'] = f"{(float(lines_statistic[n - 1]['average_speed_2']) / 60.0):5.1f}"


def change_line_stat_rollers_57(lines_statistic: list, n: int):
    lines_statistic[n - 1]['label_max_value'] = ' '
    lines_statistic[n - 1]['label_average_speed'] = ' '
    lines_statistic[n - 1]['label_made_kabel'] = ' '

    lines_statistic[n - 1]['max_value'] = ''
    lines_statistic[n - 1]['max_value_1'] = ''
    lines_statistic[n - 1]['max_value_2'] = ''

    lines_statistic[n - 1]['average_speed'] = ''
    lines_statistic[n - 1]['average_speed_1'] = ''
    lines_statistic[n - 1]['average_speed_2'] = ''

    lines_statistic[n - 1]['made_kabel'] = ''
    lines_statistic[n - 1]['made_kabel_1'] = ''
    lines_statistic[n - 1]['made_kabel_2'] = ''


def change_lines_statistic(lines_statistic:list):
    change_line_stat_twists_in_minute(lines_statistic, 6)
    change_line_stat_twists_in_minute(lines_statistic, 7)

    change_line_stat_metr_in_second(lines_statistic, 9)
    change_line_stat_metr_in_second(lines_statistic, 23)

    change_line_stat_kg_in_minute(lines_statistic, 46)
    change_line_stat_kg_in_minute(lines_statistic, 47)
    change_line_stat_kg_in_minute(lines_statistic, 48)
    change_line_stat_kg_in_minute(lines_statistic, 49)

    change_line_stat_twists_in_minute(lines_statistic, 50)

    change_line_stat_rollers_57(lines_statistic, 57)


def change_speed_lines_metr_in_second(speed_lines:list, num_lines: int):
    for minute in range(0, len(speed_lines[num_lines -1])):
        speed_lines[num_lines -1][minute] = speed_lines[num_lines -1][minute] / 60.0

def change_speed_lines(speed_lines:list):
    change_speed_lines_metr_in_second(speed_lines, 9)
    change_speed_lines_metr_in_second(speed_lines, 23)


def get_smale_speed_lines(speed_lines: list):
    result = []
    for num_lines in range(len(speed_lines)):
        result.append([])
        for minute in range(0, len(speed_lines[num_lines]), 5):
            result[num_lines].append(speed_lines[num_lines][minute])
    return result


def get_departments(lines: list):
    department_1 = sorted(filter(lambda line: line['department'] == '1', lines), key=lambda l: l["number_of_display"])
    department_2 = sorted(filter(lambda line: line['department'] == '2', lines), key=lambda l: l["number_of_display"])
    department_3 = sorted(filter(lambda line: line['department'] == '3', lines), key=lambda l: l["number_of_display"])
    # department_4 = sorted(filter(lambda line: line['department'] == 'ППК', lines), key=lambda l: l["number_of_display"])
    return [
            department_1,
            department_2,
            department_3,
            # department_4
           ]


def get_departments_ppk(lines: list):
    department_4 = sorted(filter(lambda line: line['department'] == 'ППК', lines), key=lambda l: l["number_of_display"])
    return [
            department_4
           ]


def get_data_in_select_date(select_date: dt.datetime):
    counters_values = get_counters_values_from_base(select_date)
    # print(counters_values)
    speed_lines = get_speed_lines(counters_values)
    antialiasing_speed_value(speed_lines)
    # print(speed_lines)

    lines_statistic = get_lines_statistic(speed_lines)
    # change_lines_statistic(lines_statistic)
    smale_speed_lines = get_smale_speed_lines(speed_lines)
    change_speed_lines(smale_speed_lines)
    time = [dt.time(hour=(((n * 5) // 60) + 8) % 24, minute=((n * 5) % 60)) for n, speed in
            enumerate(smale_speed_lines[0])]
    return time, smale_speed_lines, lines_statistic


def get_sorted_departments_data(departments, lines_statistic, smale_speed_lines):
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
    return out_department


def get_lines_statistic_for_date(date: dt.date):
    counters_values = get_counters_values_from_base(date)
    speed_lines = get_speed_lines(counters_values)
    antialiasing_speed_value(speed_lines)
    return get_lines_statistic(speed_lines)


def get_statistics_select_period(start_date: dt.date, step_months=1):
    end_date = start_date + relativedelta(months = step_months)

    made_kabel_in_days = []
    times = []

    if start_date:
        cur_date = start_date
        made_kabel_in_days = []
        times = []
        while cur_date < end_date:
            # print(cur_date)
            made_kabel_in_days.append([int(float(ls['made_kabel']) * 1000) for ls in get_lines_statistic_for_date(cur_date)])
            times.append(cur_date)

            cur_date = cur_date + dt.timedelta(days=1)
        # print(made_kabel_in_days)
    return times, made_kabel_in_days


def save_made_kabel_in_base(cur_date: dt.date, made_kabel: list):
    m_k = LinesStatistics()
    m_k.date = cur_date
    m_k.made_kabel = '{' + ', '.join(map(str, made_kabel)) + '}'
    m_k.save()


def create_zero_values_counters():
    return  [0 for _ in range(COUNT_LINES)]


def get_made_kabel_in_cur_month(cur_date: dt.date):
    t, made_kabel_in_days = get_statistics_select_period_and_wr_base(cur_date, step_months=1)
    made_kabel_in_cur_month = create_zero_values_counters()
    for made_kabel_in_day in made_kabel_in_days:
        made_kabel_in_cur_month = list(map(operator.add, made_kabel_in_cur_month, made_kabel_in_day))
    # print(made_kabel_in_cur_month)
    return made_kabel_in_cur_month


def get_statistics_select_period_and_wr_base(start_date: dt.date, step_months=1):
    end_date = start_date + relativedelta(months = step_months)
    made_kabel_in_days = []
    times = []
    if start_date:
        cur_date = start_date
        made_kabel_in_days = []
        times = []
        while cur_date < end_date:
            if cur_date < dt.date.today():
                if LinesStatistics.objects.filter(date=cur_date).order_by('-date').exists():
                    m_k = get_object_or_404(LinesStatistics, date=cur_date)
                    made_kabel = m_k.made_kabel
                else:
                    made_kabel = [int(float(ls['made_kabel']) * 1000) for ls in get_lines_statistic_for_date(cur_date)]
                    save_made_kabel_in_base(cur_date, made_kabel)
            elif cur_date == dt.date.today():
                made_kabel = [int(float(ls['made_kabel']) * 1000) for ls in get_lines_statistic_for_date(cur_date)]
            else:
                made_kabel = create_zero_values_counters()
            made_kabel_in_days.append(made_kabel)
            times.append(cur_date)

            cur_date = cur_date + dt.timedelta(days=1)
        # print(made_kabel_in_days)
    return times, made_kabel_in_days


def get_sorted_departments_statistic(departments, made_kabel_in_days):
    out_department = []
    for department in departments:
        out_lines = []
        for line in department:
            n = line['line_number']
            if made_kabel_in_days:
                made_kabel = [day_values[n - 1] for day_values in  made_kabel_in_days]
                sum_made_kabel = sum(made_kabel) / 1000
                made_kabel = [int(value / 1000) for value in made_kabel]
                out_lines.append({**line,
                                  'sum_made_kabel': sum_made_kabel,
                                  'made_kabel': made_kabel} )
        out_department.append(out_lines)
    return out_department
