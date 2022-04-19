import DataLevel
import DirectoryFat
from DirectoryFat import DirectoryFat
from DataLevel import Sector
from Cluster import ClusterHandle


class FatFs:
    #initialize FatFs
    def __init__(self, disk):
        self.Sector = Sector(0,disk) #open up connection to the Sector object so we can read sectors

        

        #getting the required info from the boot sector
        self.BytsPerSec = self.Sector.readLEBytes(11,2)
        self.SecPerClus = self.Sector.readLEBytes(13,1)
        self.RsvdSecCnt = self.Sector.readLEBytes(14,2)
        self.NumFATs = self.Sector.readLEBytes(16,1)
        self.TotSec32 = self.Sector.readLEBytes(32,4)
        
        #Extended Variables
        self.FATSz32 = self.Sector.readLEBytes(36,4)
        self.RootClus = self.Sector.readLEBytes(44,4)
        
        self.ClusterHandle = ClusterHandle(self.RsvdSecCnt,self.RsvdSecCnt + self.FATSz32,disk)
        self.DirectoryFat = DirectoryFat(disk) #create the Directory Fat object

    def newFile(self,dirName):
        first = self.ClusterHandle.newCluster()
        self.DirectoryFat.createDir(dirName,first)
    

