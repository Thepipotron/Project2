
import time
import board
import adafruit_lis3mdl

def getMAGCombined(i2c):
    sensor = adafruit_lis3mdl.LIS3MDL(i2c)
    mag = sensor.magnetic
    message = str(mag[0]) + "," + str(mag[1]) + "," + str(mag[2])
    return message