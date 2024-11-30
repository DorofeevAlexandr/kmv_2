from datetime import datetime

from sqlalchemy.sql.functions import session_user

from read_counter import (read_input_registers_modbus_device, get_connection, get_indicator_value,
                          get_plc_indicator_value, get_plc_connection)
import time as _time

from models import Lines, LinesCurrentParams



COUNTER_SIMULATION = True

def get_speed(dt_old, length, old_length):
    if dt_old is None:
        return None
    dt = datetime.now() - dt_old
    seconds = dt.total_seconds()
    if seconds == 0:
        return 0
    else:
        return 60.0 * (length - old_length) / seconds


def read_serial_port_counters(session, lines_params):
    for line in lines_params:
        if line['port'] == 'ttyS0':
            port = '/dev/ttyS0'
        elif line['port'] == 'ttyS1':
            port = '/dev/ttyS1'
        else:
            continue

        if COUNTER_SIMULATION:
            ind_value = datetime.now().second
            conected = False
        else:
            registers = read_input_registers_modbus_device(port=port,
                                                           slave_adr=line['modbus_adr'])
            ind_value = get_indicator_value(registers)
            conected = get_connection(registers)

        length = ind_value * line['k'] 
        update_line_in_base(session, line,
                            ind_value=ind_value,
                            conected=conected,
                            length=length)

def read_plc_counters(session, lines_params, registers):
    for line in lines_params:
        if line['port'] == 'SL1' or line['port'] == 'SL2':
            if COUNTER_SIMULATION:
                ind_value = datetime.now().second
                conected = False
            else:
                ind_value = get_plc_indicator_value(registers, line['line_number'])
                conected = get_plc_connection(registers, line['line_number'])

            length = ind_value * line['k']
            update_line_in_base(session, line,
                                ind_value=ind_value,
                                conected=conected,
                                length=length)
        else:
            continue

def read_lines_params_in_base(session):
    params = []
    lines = session.query(Lines).all()
    for line in lines:
        params.append({
            'id' : line.id,
            'line_number' : line.line_number,
            'name' : line.name,
            'pseudonym' : line.pseudonym,
            'port' : line.port,
            'modbus_adr' : line.modbus_adr,
            'department' : line.department,
            'number_of_display' : line.number_of_display,
            'cable_number' : line.cable_number,
            'cable_connection_number' : line.cable_connection_number,
            'k' : line.k,
            'created_dt' : line.created_dt,
            'description' : line.description,
            })
    return params

def read_lines_current_params_in_base(session, line_number):
    line = session.query(LinesCurrentParams).filter(LinesCurrentParams.line_number==line_number).first()
    if line:
        params = {
            'id' : line.id,
            'line_number' : line.line_number,
            'no_connection_counter' : line.no_connection_counter,
            'indicator_value' : line.indicator_value,
            'length' : line.length,
            'speed_line' : line.speed_line,
            'updated_dt' : line.updated_dt,
            }
        return params

def update_line_in_base(session, line_params, ind_value=0, conected=False, length=0):
    line_number = line_params['line_number']
    if current_params := read_lines_current_params_in_base(session, line_number):
        speed_line = get_speed(current_params['updated_dt'], length, current_params['length'])
    else:
        speed_line = 0
    line = session.query(LinesCurrentParams).filter(LinesCurrentParams.line_number==line_number).first()
    if line:
        line.indicator_value = ind_value
        line.no_connection_counter = not conected
        line.length = length
        line.speed_line = speed_line
        line.updated_dt = datetime.now()
    else:
        line = LinesCurrentParams(line_number=line_params['line_number'])
    session.add(line)
    session.commit()


