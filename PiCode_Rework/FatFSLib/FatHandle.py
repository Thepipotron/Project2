import DataLevel
import DirectoryFat
from DirectoryFat import DirectoryFat
from DataLevel import Sector
from Cluster import ClusterHandle
from DataHandle import Data


class FatFs:
    #initialize FatFs
    def __init__(self, disk):
        self.Sector = Sector(0,disk) #open up connection to the Sector object so we can read sectors
        self.Disk = disk
        

        #getting the required info from the boot sector
        self.BytsPerSec = self.Sector.readLEBytes(11,2)
        self.SecPerClus = self.Sector.readLEBytes(13,1)
        self.RsvdSecCnt = self.Sector.readLEBytes(14,2)
        self.NumFATs = self.Sector.readLEBytes(16,1)
        self.TotSec32 = self.Sector.readLEBytes(32,4)
        
        #Extended Variables
        self.FATSz32 = self.Sector.readLEBytes(36,4)
        self.RootClus = self.Sector.readLEBytes(44,4)

        #first data sector
        self.FirstDat = self.RsvdSecCnt + (self.NumFATs * self.FATSz32)
        
        self.ClusterHandle = ClusterHandle(self.RsvdSecCnt,self.RsvdSecCnt + self.FATSz32,disk)
        self.DirectoryFat = DirectoryFat(disk) #create the Directory Fat object

    #function to create new file and set the FATfs pointers to said file
    def newFile(self,dirName):
        first = self.ClusterHandle.newCluster()
        self.DirectoryFat.createDir(dirName,first)
        #compute the cluster sector

        firstSectorCluster = ((first-2) * self.SecPerClus) + self.FirstDat

        self.Data = Data(firstSectorCluster,self.Disk)

    #function to write to a newly created file. Data is a string
    def writeFile(self, data):
        #first encode the string as a bunch of bytes
        bData = bytearray(data, 'utf-8')

        #attempt to write the data with no new cluster allocation
        res = self.Data.writeDat(bData)

        #assume for now that at most data will only splill over 1 cluster
        if res > 0:
            cluster = self.ClusterHandle.reallocate() #give the file another cluster
            firstSectorCluster = ((cluster-2) * self.SecPerClus) + self.FirstDat

            self.Data.changeSector(firstSectorCluster) #get the new data cluster
            self.Data.writeDat(bData[len(bData)-res:len(bData)])
        
        #assume all data is written add filesize to the directory
        self.DirectoryFat.addSize(len(bData))



    

