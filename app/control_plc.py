from dotenv import load_dotenv
import os
from pyModbusTCP.client import ModbusClient
import time
from threading import Thread, Lock


load_dotenv()
PLC_HOST = os.environ.get('PLC_HOST')
PLC_PORT = 502

# set global
regs = {key: 0 for key in range(0, 700)}
print(regs)

stack_of_writable_register = []

# init a thread lock
regs_lock = Lock()

# modbus polling thread
def polling_thread():
    global regs
    c = ModbusClient(host=PLC_HOST, port=PLC_PORT)
    # polling loop
    while True:
        # keep TCP open
        if not c.is_open():
            c.open()
        # do modbus reading on socket
        reg_list_0 = c.read_holding_registers(0, 100)
        reg_list_1 = c.read_holding_registers(100, 100)
        reg_list_2 = c.read_holding_registers(200, 100)
        reg_list_3 = c.read_holding_registers(300, 100)
        reg_list_4 = c.read_holding_registers(400, 100)
        reg_list_5 = c.read_holding_registers(500, 100)
        reg_list_6 = c.read_holding_registers(600, 100)

        # if read is ok, store result in regs (with thread lock synchronization)
        if reg_list_0 and reg_list_1 and reg_list_2 and reg_list_3 and reg_list_4 and reg_list_5 and reg_list_6:
            with regs_lock:
                for i in range(0, 100):
                    regs[0 + i] = reg_list_0[i]
                for i in range(0, 100):
                    regs[100 + i] = reg_list_1[i]
                for i in range(0, 100):
                    regs[200 + i] = reg_list_2[i]
                for i in range(0, 100):
                    regs[300 + i] = reg_list_3[i]
                for i in range(0, 100):
                    regs[400 + i] = reg_list_4[i]
                for i in range(0, 100):
                    regs[500 + i] = reg_list_5[i]
                for i in range(0, 100):
                    regs[600 + i] = reg_list_6[i]

                while stack_of_writable_register:
                    regs_addr, regs_values = stack_of_writable_register.pop()
                    print('write->', regs_addr, regs_values)
                    c.write_multiple_registers(regs_addr, regs_values)

        # 5s before next polling
        time.sleep(5)

def get_registers():
    with regs_lock:
         result = regs.copy()
    return result

def write_register(reg_adr: int, new_value: int):
    stack_of_writable_register.append((reg_adr, new_value))


# start polling thread
tp = Thread(target=polling_thread)
# set daemon: polling thread will exit if main thread exit
tp.daemon = True
tp.start()


if __name__ == '__main__':
    while True:
        get_registers()
        write_register(reg_adr=1, new_value=123)
        time.sleep(1)
