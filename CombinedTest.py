#This is to test the BTooth and USB functions together in the same program


import time
from BTooth import sendBtooth
import serial
import BTooth.py
import USB.py

string = "This is to be sent by BTooth\r\n"
sendBtooth(string)
string2 = "This is to be sent by USB\r\n"
sendUSB(string2)