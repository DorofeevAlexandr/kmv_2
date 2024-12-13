import csv
from datetime import datetime, timedelta
import os


def append_in_csv(lines_name: list, current_lengths: list):
    shift_hours = 8
    file_name = create_dir(shift_hours=8)
    write_header = not os.path.exists(file_name)
    with open(file_name, mode="a", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter = ";", lineterminator="\r")
        st_time = str((datetime.now() - timedelta(hours=shift_hours)).hour) + ':' + str(datetime.now().minute)
        if write_header:
            s = 'Time - 7h;RAS040;RAS041;RAS042;RAS032;RAS033;RAS034.1;RAS034.2;RAS035;RAS038;RAS039;REW1400;AV120;AV90;TB1600;TB63;REW2000;RAS047;RAS043;RAS036;T8;N-7;Lj400;SKETT;JLG 630/1+12;JLG (1+6)*630;JLK 630/12+18+24 B;AKZ-600;GT 120+45;JPD-2200;GT 120+120;FR ¹1;FR ¹2;FR ¹3;FR ¹4;FR ¹5;FR ¹6;FR ¹7;SETIC-630;LBK ¹2;SAMP-800;RAS044;WINDAK;DAK;NB 1250;T 40;PVH;Polietilen;Katalizator;Rezina;800 ¹2;FR ¹8;FR ¹9;LBK ¹4;Linda;120+45 ¹2;80+45;Valcy;Hibrid'
            file_writer.writerow(s)
            # file_writer.writerow(['Time - 7h'] + [line[0] for line in lines_name])
        file_writer.writerow([st_time] + [str(int(c_length[0] * 1000)) for c_length in current_lengths])

def create_dir(shift_hours=0):
    dt = datetime.now() - timedelta(hours=shift_hours)
    year = str(dt.year)
    month = str(dt.month)
    day = str(dt.day)
    file_name = 'Lines_data_' + year + '_' + month + '_' + day + '.csv'
    # basedir = os.path.abspath(os.path.dirname(__file__))
    basedir = '/var/data_base_csv'
    path = os.path.join(basedir,'USER1','sd0' , year, month)
    file_name = os.path.join(path, file_name)
    if not os.path.isdir(path):
        os.makedirs(path)   
    return file_name
