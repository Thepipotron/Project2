import busio
from board import *
from adafruit_bus_device.i2c_device import I2CDevice
import time

def computeChksum(bData):
    ck_a = 0
    ck_b = 0

    for i in range(0,len(bData)):
        ck_a = (ck_a + bData[i]) & 0xff
        ck_b = (ck_b + ck_a) & 0xff

    return ck_a.to_bytes(1,'big') + ck_b.to_bytes(1,'big') 

class GPS:
    def __init__(self,i2c):
        self.device =  I2CDevice(i2c, 0x42) #init an i2c device here

    #get all gps data
    def getGPSCombined(self):
        self.getData()

        lock = self.getLock()

        coords = self.getCoords()

        ele = self.getElevation()

        return lock + "," + coords + "," + ele

    def wakeUp(self):
        msg = 0xB5.to_bytes(1,'big') +  0x62.to_bytes(1,'big') + 0x06.to_bytes(1,'big') + 0x00.to_bytes(2,'big')+0x01.to_bytes(2,'little') + 0x00.to_bytes(1,'little')
        cksum = computeChksum(msg)
        msg += cksum
        print(msg)
        self.device.write(bytearray(msg))

    #tell how many satellites the GPS is currently locked to
    def getLock(self):
        start = self.data.find('$GPGGA') #start of substring
        end = self.data.find('\r\n',start) #end of substring
        gga = self.data[start:end]

        gga = gga.split(',')
        print(gga)
        return gga[7]
    
    #returns the coordinates of the current GPS location. if no coordinates then return [0,0]
    def getCoords(self):
        start = self.data.find('$GPGGA') #start of substring
        end = self.data.find('\r\n',start) #end of substring
        gga = self.data[start:end]
        gga = gga.split(',')

        ns = gga[2]
        nsIndicator = gga[3]
        ew = gga[4]
        ewIndicator = gga[5]

        #if there is no data then return ['0N','0W']
        if ns == '':
            return '0,0,N,0,0,E'

        #construct the coord string
        coordNs = ns[0:2] + "," + ns[2:len(ns)] + "," + nsIndicator  
        coordEw = ew[0:3] + "," + ew[3:len(ew)] + "," + ewIndicator 

        return coordNs + "," +coordEw

    def getElevation(self):
        start = self.data.find('$GPGGA') #start of substring
        end = self.data.find('\r\n',start) #end of substring
        gga = self.data[start:end]
        gga = gga.split(',')

        ele = gga[9]
        if ele == '':
            return '0'
        return ele


    
    def getBufferSize(self):
        resHI = bytearray(1)
        try :
            self.device.write(0xfd.to_bytes(1,'big'))
        except:
            return -1

        self.device.readinto(resHI)
        resLO = bytearray(1)

        try:
            self.device.write(0xfe.to_bytes(1,'big'))
        except:
            return -1

        self.device.readinto(resLO)
        res = int.from_bytes(resHI + resLO,'big')
        
        if res == 0: #if there is no data wait and recall
            time.sleep(.2)
            return self.getBufferSize()

        return res

    def resetBuffer(self):
        time.sleep(2.5)
        self.wakeUp()
        

    #returns the raw bytes in the data buffer
    def getData(self):
        datSize = self.getBufferSize()

        if datSize == -1:
            self.resetBuffer()
            return self.getData()

        res = bytearray(0)
        buff = bytearray(1)
        print(datSize)
        for i in range(0,datSize):
            try:
                self.device.write(0xff.to_bytes(1,'big'))
            except:
                self.resetBuffer() #try again
                return self.getData()

            self.device.readinto(buff)
            res += buff   
        self.data = res.decode('utf-8') #reads raw data into object as a string
        if self.data.find('$GPGGA') == -1:
            self.resetBuffer()
            return self.getData()
