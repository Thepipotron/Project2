from DataLevel import *

#object points to both clusters in both fats
class ClusterHandle:
    def __init__(self,startSector1,startSector2, disk):
        Sector1 = Sector(startSector1,disk) #access to the first FAT
        Sector2 = Sector(startSector2,disk) #access to the second FAT

        FSInfoSector1 = Sector(1,disk) #access to the FSInfo1 table 
        FSInfoSector2 = Sector(7,disk) #access to the FSInfo2 table 

        self.Cluster = Cluster(Sector1,Sector2)
        self.FSInfo = FSInfo(FSInfoSector1,FSInfoSector2)
        
    
    #allocate a new cluster used for creating a new file
    def newCluster(self):
        #start by getting the first cluster availible
        First = self.FSInfo.FirstAvail
        print("Fisrt : " + str(First))
        #allocate the cluster (let filesystem know the cluster is no longer free)
        self.Cluster.allocate(First)
        #increment first file avail and dec avail cluster
        self.FSInfo.incAvailCluster()
        
        #update Cluster and FSInfo with the new bytes
        self.Cluster.validate()
        self.FSInfo.validate()

        #return cluster number of allocated cluster
        return First
    #give the  file currently pointed at a new cluster
    def reallocate():
        First = self.FSInfo.FirstAvail

        self.Cluster.reallocate(First)
        self.FSInfo.incAvailCluster()

        self.Cluster.validate()
        self.FSInfo.validate()

        return First



class FSInfo:
    def __init__(self, Sector1,Sector2):
        self.Sector1 = Sector1
        #self.Sector2 = Sector2
        #raw bytes to minimise Reads
        self.validate()
        print(self.SectorAvail)
    
    #increment the first availible cluster counter and decrement the sector availible count
    def incAvailCluster(self):
        self.Sector1.writeBytes(492,convertLE(self.FirstAvail + 1,4),4)
        #self.Sector2.writeBytes(492,convertLE(self.FirstAvail + 1,4),4)
        self.FirstAvail += 1
        self.Sector1.writeBytes(488,convertLE(self.SectorAvail - 1,4),4)
        #self.Sector2.writeBytes(488,convertLE(self.SectorAvail - 1,4),4)
        self.SectorAvail -= 1

    #grabs any updated data from the FS
    def validate(self):
        self.RawBytes = self.Sector1.readBytes(0,512)
        self.FirstAvail = self.Sector1.readLEBytes(492,4)
        self.SectorAvail = self.Sector1.readLEBytes(488,4)




class Cluster:
    def __init__(self, Sector1, Sector2):
        self.Sector1 = Sector1
        self.Sector2 = Sector2
        #raw bytes to minimise Reads
        self.validate()
    
    #used to allocate new cluster to a new file
    def allocate(self,firstAvail):
        offset = firstAvail * 4 #byte offset of first availible cluster
        self.cluster = firstAvail #point the cluster number to the newly created file
        self.Sector1.writeBytes(offset, convertLE(0x0fffffff,8),8)
        self.Sector2.writeBytes(offset, convertLE(0x0fffffff,8),8)
    
    #add more space to an existing file input the cluster number of the first cluster in the file
    def reallocate(self,firstAvail):
        #first change the current cluster info to point to the new cluser
        offset = cluster * 4
        self.Sector1.writeBytes(offset, convertLE(firstAvail,8),8)
        self.Sector2.writeBytes(offset, convertLE(firstAvail,8),8)

        #next allocate the new cluster to the file
        self.allocate(firstAvail)

        

    #grab the new data from the disk
    def validate(self):
        self.RawBytes = self.Sector1.readBytes(0,512)


