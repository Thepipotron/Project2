
import board
from adafruit_lsm6ds.lsm6ds33 import LSM6DS33

def getIMUCombined(i2c):
    sensor = LSM6DS33(i2c)
    return sensor.acceleration + sensor.gyro