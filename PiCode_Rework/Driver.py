import IMU
import MAG
import board
import busio
import os
import sys

sys.path.insert(1, '/home/pi/Project2/PiCode_Rework/FatFSLib')

from FatHandle import FatFs, DirectoryFat
from DataLevel import *

disk = Disk()

fat = FatFs(disk)

#print(hex(readLEBytes(fat.ClusterHandle.Cluster.RawBytes,7*4,4)))
#print(fat.ClusterHandle.Cluster.RawBytes)
print(fat.DirectoryFat.Sector.readBytes(0,512))

fat.newFile('data.txt')

print(fat.DirectoryFat.Sector.readBytes(0,512))
print(fat.ClusterHandle.Cluster.Sector1.readBytes(0,512))

