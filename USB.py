import serial
import time


def sendUSB(str):
    device = serial.Serial(port = '/dev/ttyGS0', baudrate=9600)
    time.sleep(.1)
    if device.isOpen():
        print ("USB is open\r\n")
        str2 = str.encode()
        device.write(str2)
        print("message: " + str + " has been sent\r\n")
        device.close()
    else: 
        print ("USB did not open\r\n")


