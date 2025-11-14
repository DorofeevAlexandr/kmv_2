import datetime as dt
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import time

import control_plc
from save_csv_file import append_in_csv
from wear_lines import (read_lines_params_in_base, read_plc_counters, read_serial_port_counters,
                        read_current_lengths_in_base, read_current_connections_in_base, read_lines_name,
                        add_in_base_counters)


def postgres_engine():
    load_dotenv()
    db_name = os.environ.get('DB_NAME')
    db_user = os.environ.get('DB_USER')
    db_pass = os.environ.get('DB_PASSWORD')
    db_host = os.environ.get('DB_HOST', 'db')
    # db_host = 'localhost'
    db_port = str(os.environ.get('DB_PORT', 5432))

    # Connecto to the database
    db_string = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
    # print(db_string)
    result_engine = create_engine(db_string)
    print(result_engine)
    return result_engine

def read_counters_save_current_params(p_engine):
    with Session(autoflush=False, bind=p_engine) as db:

        registers = control_plc.get_registers()
        lines_params = read_lines_params_in_base(session=db)
        # print(lines_params)
        read_plc_counters(db, lines_params, registers)
        read_serial_port_counters(db, lines_params)
        try:
            pass
        except Exception as e:
            print('error', e)

def read_current_params_save_in_base(p_engine):
    with Session(autoflush=False, bind=p_engine) as db:
        current_lengths = read_current_lengths_in_base(db)
        # print(current_lengths)
        current_connections = read_current_connections_in_base(db)
        # print(current_connections)
        lines_name = read_lines_name(db)
        # print(lines_name)

        append_in_csv(lines_name=lines_name, current_lengths=current_lengths)
        add_in_base_counters(db, current_lengths=current_lengths, current_connections=current_connections)
        try:
            pass
        except Exception as e:
            print('error', e)

if __name__ == '__main__':
    engine = postgres_engine()
    dt_last_save_current_params = dt.datetime.now()
    dt_last_save_lengths = dt.datetime.now()
    while True:
        time.sleep(1)

        if ((0 < dt.datetime.now().second < 30 ) and
                (dt.datetime.now() - dt_last_save_lengths > dt.timedelta(seconds=30))):
            dt_last_save_lengths = dt.datetime.now()
            # print('dt_last_save_lengths', dt_last_save_lengths)
            read_current_params_save_in_base(p_engine=engine)

        if dt.datetime.now() - dt_last_save_current_params >= dt.timedelta(seconds=30):
            read_counters_save_current_params(p_engine=engine)
            dt_last_save_current_params = dt.datetime.now()
            # print('read_counters_save_current_params', dt_last_save_current_params)
