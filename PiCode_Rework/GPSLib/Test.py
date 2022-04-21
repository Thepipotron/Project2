import busio
from board import *
from adafruit_bus_device.i2c_device import I2CDevice
import time
from GPS import GPS



with busio.I2C(SCL, SDA) as i2c:
    device = I2CDevice(i2c, 0x42)
    GPS = GPS(busio.I2C(SCL, SDA))
    bytes_read = bytearray(4)
    # A second transaction
    with device:
        #start by constructing a bytesream for the message we want to send
        
        while 1:
            print(GPS.getGPSCombined())
       
        #device.write(0xfd.to_bytes(1,'little'))
        #device.readinto(res)
        #print(res)

        