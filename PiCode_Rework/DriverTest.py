#!/usr/bin/env python
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
import digitalio

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
        print("disk done")
        fat = FatFs(disk)
        print("Fat created")
        fat.newFile('DATA.CSV')
        print("file created")
    #Write the headers to the file
        fat.writeFile("Date,Time,Locked GPS,Latitude deg,Latitude min,N/S,Longitude deg,Longitude min,W/E,MSL Elevation,X_ACC (m/s^2),Y_ACC (m/s^2),Z_ACC (m/s^2),")
        fat.writeFile("X_GYRO (rps),Y_GYRO (rps),Z_GYRO (rps),X_MAG (uT),Y_MAG (uT),Z_MAG (uT)\r\n")
    except:
        sd = 0 #no sd card detected

    while 1:
        pass
        #check for sd card good to remove
        if(buttonCheck.value == 0):
            sd = 0
            ledSafe.value = 1
        
        #initialize gpsu
        I2C = board.I2C()
        gps = GPS(busio.I2C(SCL, SDA))
        

        print("Getting GPS")
        gpsInfo = gps.getGPSCombined()
        lock = int(gps.getLock())
        now = datetime.now()
        
        if lock > 3:
            ledGPS.value = 1
        else:
            ledGPS.value = 0

       
        magInfo = MAG.getMAGCombined(I2C)
        accInfo = IMU.getIMUCombined(I2C)

       
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S").split(' ')

        string = dt_string[0] + "," + dt_string[1] + "," + gpsInfo + "," +accInfo + "," + magInfo +"\r\n"
        BTooth.sendBtooth(string)

        try:
            USB.sendUSB(string)
        except:
            pass

        if sd == 1:
            print("sd is printing\r\n")
            try:
                fat.writeFile(string)
            except:
                pass

#initialize button for SD card
buttonCheck = digitalio.DigitalInOut(board.D4)
buttonCheck.direction = digitalio.Direction.INPUT
buttonCheck.pull = digitalio.Pull.UP

#initialize GPS Lock LED
ledGPS = digitalio.DigitalInOut(board.D5)
ledGPS.direction = digitalio.Direction.OUTPUT

#intiialize Safe to pull SD LED
ledSafe = digitalio.DigitalInOut(board.D6)
ledSafe.direction = digitalio.Direction.OUTPUT


time.sleep(1)


ledGPS.value = 1

main()