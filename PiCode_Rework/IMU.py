
import board
from adafruit_lsm6ds.lsm6ds33 import LSM6DS33

def getIMUCombined(i2c):
    sensor = LSM6DS33(i2c)
    acc = sensor.acceleration
    gyro = sensor.gyro
    message = str(acc[0]) + "," + str(acc[1]) + "," + str(acc[2]) + "," str(gyro[0]) + "," + str(gyro[1]) + "," + str(gyro[2])
    return message