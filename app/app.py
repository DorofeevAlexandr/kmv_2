import time
from multiprocessing.reduction import register

import control_plc


while True:
    registers = control_plc.get_registers()
    print(registers)
    control_plc.write_register(reg_adr=1, new_value=123)
    time.sleep(1)