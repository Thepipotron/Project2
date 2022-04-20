#This is to test the BTooth and USB functions together in the same program


import time
from BTooth import sendBtooth
import serial
import BTooth
import USB

string = "This is to be sent by BTooth\r\n"
BTooth.sendBtooth(string)
string2 = "This is to be sent by USB\r\n"
USB.sendUSB(string2)