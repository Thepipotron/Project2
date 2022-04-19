
import time
import board
import adafruit_lis3mdl

def getMAGCombined(i2c):
    sensor = adafruit_lis3mdl.LIS3MDL(i2c)
    return sensor.magnetic