

import serial
import time

def sendBtooth(str):
    device = serial.Serial(port = '/dev/ttyS0', baudrate=9600)
    time.sleep(.1)
    if device.isOpen():
        print ("Bluetooth is open\r\n")
        str2 = str.encode()
        device.write(str2)
        print("message: " + str + " has been sent\r\n")
        device.close()
    else: 
        print ("Bluetooth did not open\r\n")

