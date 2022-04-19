

#Bluetooth Module 

#Connections

#State -------- No Connection
#RXD ---------- GPIO15 (UART RX)
#TXD ---------- GPIO14 (UART TX)
#GND ---------- Ground
#VCC ---------- 5V
#EN ----------- No Connection



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

string1 = "This is the first test\r\n"
string2 = "Now this is the second\r\n"
string3 = "And finally the third\r\n"
sendBtooth(string1)
sendBtooth(string2)
sendBtooth(string3)