import sys
import BTooth
import USB
import threading
import time
import MAG
import IMU
import board
from datetime import datetime
import busio
from board import *

sys.path.append('/home/pi/Project2/PiCode_Rework/GPSLib')
sys.path.append('/home/pi/Project2/PiCode_Rework/FatFSLib')

from GPS import GPS
from FatHandle import FatFs
from DataLevel import Disk


def main():
    sd = 1
    #setup fatfs filesystem
    try:
        disk = Disk()
        fat = FatFs(disk)
        fat.newFile('DATA.CSV')

    #Write the headers to the file
        fat.writeFile("Date,Time,Locked GPS,Latitude deg,Latitude min,N/S,Longitude deg,Longitude min,W/E,MSL Elevation,X_ACC (m/s^2),Y_ACC (m/s^2),Z_ACC (m/s^2),")
        fat.writeFile("X_GYRO (rps),Y_GYRO (rps),Z_GYRO (rps),X_MAG (uT),Y_MAG (uT),Z_MAG (uT)\r\n")
    except:
        sd = 0 #no sd card detected

    while 1:
        pass
        
        I2C = board.I2C()
        gps = GPS(busio.I2C(SCL, SDA))
        
        gpsInfo = gps.getGPSCombined()
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S").split(' ')
        #magInfo = MAG.getMAGCombined(I2C)
        #accInfo = IMU.getIMUCombined(I2C)




        string = dt_string[0] + "," + dt_string[1] + "," + gpsInfo + "\r\n"
        BTooth.sendBtooth(string)

        try:
            USB.sendUSB(string)
        except:
            pass

        if sd == 1
            try:
                fat.writeFile(string)
            except:
                pass


main_thread = threading.Thread(name='main program',
                               target=main, daemon=True)
main_thread.start()


while True:
    if input().lower() == 'kill':
        print('Terminating program')
        sys.exit(0)