from pickle import TRUE
import IMU
import MAG
import board
import busio
import os
import sys
import BTooth
import USB
import threading

sys.path.insert(1, '/home/pi/Project2/PiCode_Rework/FatFSLib')

from FatHandle import FatFs, DirectoryFat
from DataLevel import *

disk = Disk()

fat = FatFs(disk)

#print(hex(readLEBytes(fat.ClusterHandle.Cluster.RawBytes,7*4,4)))
#print(fat.ClusterHandle.Cluster.RawBytes)
print(fat.DirectoryFat.Sector.readBytes(0,512))
print(fat.ClusterHandle.Cluster.RawBytes)

print(fat.FirstDat)
print(fat.SecPerClus)
S = Sector(65548,disk)
print(S.readBytes(0,512))

fat.newFile('DATA.TXT')
writes = 0
while writes < 1000:
    fat.writeFile('write #: ' + str(writes) + '\r\n')
    writes+=111
    print(writes)


