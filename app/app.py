from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import time

import control_plc
from wear_lines import read_lines_params_in_base, read_plc_counters, read_serial_port_counters


def postgres_engine():
    load_dotenv()
    db_name = os.environ.get('DB_NAME')
    db_user = os.environ.get('DB_USER')
    db_pass = os.environ.get('DB_PASSWORD')
    # db_host = os.environ.get('DB_HOST', 'db')
    db_host = 'localhost'
    db_port = str(os.environ.get('DB_PORT', 5432))

    # Connecto to the database
    db_string = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
    print(db_string)
    result_engine = create_engine(db_string)
    print(result_engine)
    return result_engine

def read_counters_save_current_params(p_engine):
    with Session(autoflush=False, bind=p_engine) as db:

        registers = control_plc.get_registers()
        print(registers)
        control_plc.write_register(reg_adr=1, new_value=123)
        lines_params = read_lines_params_in_base(session=db)
        print(lines_params)
        read_plc_counters(db, lines_params, registers)
        read_serial_port_counters(db, lines_params)
        try:
            pass
        except Exception as e:
            print('error', e)

if __name__ == '__main__':
    time.sleep(1)
    engine = postgres_engine()
    while True:
        read_counters_save_current_params(p_engine=engine)
        time.sleep(10)

