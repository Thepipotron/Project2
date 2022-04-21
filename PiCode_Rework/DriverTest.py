from pickle import TRUE
import sys
import BTooth
import USB
import threading
import time
import MAG
import IMU
import board
from datetime import datetime


def main():
    while TRUE:
        pass
        
        I2C = board.I2C()
        mag_x, mag_y, mag_z = MAG.getMAGCombined(I2C)
        Acc_x, Acc_y, Acc_z, Gy_x, Gy_y, Gy_z = IMU.getIMUCombined(I2C)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        string = ""
        BTooth.sendBtooth(string)
        USB.sendUSB(string)
        time.sleep(10)


main_thread = threading.Thread(name='main program',
                               target=main, daemon=True)
main_thread.start()
while True:
    if input().lower() == 'kill':
        print('Terminating program')
        sys.exit(0)