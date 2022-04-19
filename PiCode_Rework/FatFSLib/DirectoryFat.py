import DataLevel
from DataLevel import *
import math
from datetime import datetime,date
import sys



#helper function to get the current date in a formatted string of bytes
def getDate():
    now = datetime.now()
    year = now.date().year - 1980
    month = now.date().month
    day = now.date().day


    fullDate = year << 9 | month << 5 | day
    return convertLE(fullDate,2) 

    

#helper function to get the current time in a formatted string of bytes
def getTime():
    now = datetime.now()
    hr = now.time().hour
    mte = now.time().minute
    sec = int((now.time().second - 1)/2)

    fullTime = hr << 11 | mte << 5 | sec
    return convertLE(fullTime,2)


#Class that contains the entire directory (Long and short) for a given file
class DirectoryFat:
    def __init__(self,disk):
        self.disk = disk
        self.offset = 0 #start of the current FULL directory
        self.Sector = Sector(5150+(30193*2),disk) #Access to the sector object initialized at the directory sector
        self.validate()
            
    def nextDir(self):
        self.offset += 32*(self.dirSize+1)
        self.validate()

    def getFileName(self):
        return 0

    #assumes that there is always a long dir before the short dir (there should be owo)
    def findDirLength(self):
        res = self.Sector.readLEBytes(self.offset,1)
        if(res == 0xE5):
            return -2
        res = res &  ~ 0x40
        if(res == 0x00):
            return -2
        return res

    def validate(self):
        self.dirSize = self.findDirLength() #size in number of entries of this directory
        self.LongDirs = []
        self.ShortDir = ShortDir(self.dirSize,self.Sector,self)
        self.LongDirName = bytearray(0)
        #create LongDir objects for each long directory entry
        for c in range(0,self.dirSize):
            self.LongDirs.append(LongDir(c,self.Sector,self))
        
        for LongD in reversed(self.LongDirs):
            self.LongDirName += LongD.DirName

    #create a new Dir entry at the end of the list with name of dir = dirName
    def createDir(self, dirName, cluster):
        dirNameLength = len(dirName)

        #find the first avail directory
        while(self.findDirLength() != -2):
            self.nextDir()

        #calculate the number of dir's needed (includes short dir)
        count = math.ceil(float(dirNameLength) / 13.0) + 1 

        
        if(dirNameLength > 10):
            print("ERR: Name too long")
            return
        
        #start by creating  the short dir
        newShortDir = ShortDir.createShortDir(dirName,cluster)
        newLongDir = LongDir.createLongDir(dirName,newShortDir)

       

        newDir = newLongDir + newShortDir
        print(newDir)
        print(len(newDir))
        print(self.offset)

        self.Sector.writeBytes(self.offset,newDir,64)
        self.validate() #re grab the data from the current directory

    def addSize(self,size):
        #start by getting the current size of the file 
        currSize = self.ShortDir.FileSize

        #write the new file size and validate
        self.Sector.writeBytes(self.offset+32+28,convertLE(currSize+size,4),4)

    #implement later. makes the directory object point to a directory the user is writing to
    #def openDir()

    

#Class for the long Directoy objects in the Directory Table
#pos position relative to DirectoryFat starting at 0
class LongDir:
    def __init__(self, pos, Sector, DirectoryFat):
        self.DirectoryFat = DirectoryFat
        self.offset = self.DirectoryFat.offset + (32*pos) #gives the offset for this dir
        self.RawBytes = Sector.readBytes(self.offset,32) #raw bytes for this dir entry
        self.DirName = readBytes(self.RawBytes,1,10) + readBytes(self.RawBytes,14,12) + readBytes(self.RawBytes,28,4)
        self.Attr = readLEBytes(self.RawBytes,11,1)
        #check to make sure this dir is still within the sector
        if(self.offset > 512-32):
            self.sector += 1
            self.offset = 0

    def createLongDir(dirName,ShortDirBytes):
        fullEntry = bytearray(convertLE(0x41,1))
        #split dirname into the appropiate byte array
        splitDirName = [char for char in dirName]
        NameDone = 0
        formattedFileName = bytearray(0)

        #construct the name of the file
        for c in range(0,len(splitDirName)):
            formattedFileName += bytearray(splitDirName[c],'utf-8') + convertLE(0,1)
        
        formattedFileName += convertLE(0x0000,2)

        for c in range(0,13-len(splitDirName)-1):
            formattedFileName += convertLE(0xffff,2)

        fullEntry += formattedFileName[0:10]
        fullEntry += convertLE(0x0f,1)
        fullEntry += convertLE(0x00,1)
        #calculate the Checksum
        ShortFileName = readBytes(ShortDirBytes,0,11)
        Sum = 0
        for FcbNameLen in range(11,0,-1):
            addBit = 0
            if((Sum & 0x01) != 0):
                addBit = 0x80
            else:
                addBit = 0
            Sum =  ((Sum>>1) +addBit  + readLEBytes(ShortFileName,11-FcbNameLen,1)) & 0xff

        fullEntry += convertLE(Sum,1)
        fullEntry += formattedFileName[10:23]
        fullEntry += convertLE(0x00,2)
        fullEntry += formattedFileName[23:26]
        return fullEntry

                



        

class ShortDir:
    def __init__(self,pos,Sector,DirectoryFat):
        self.DirectoryFat = DirectoryFat
        self.offset = self.DirectoryFat.offset + (32*pos)
        self.RawBytes = Sector.readBytes(self.offset,32)
        self.DirName = readBytes(self.RawBytes,0,11) #read the name of the shortfile from Disk
        self.DirAttr = readBytes(self.RawBytes,11,1)
        self.CreateMonth = readBytes(self.RawBytes,16,2)
        self.FstClusLO = readLEBytes(self.RawBytes,26,2)
        self.FileSize = readLEBytes(self.RawBytes,28,4)
        #check to make sure this dir is still within the sector
        if(self.offset > 512-32):
            self.sector += 1
            self.offset = 0

    #returns the bytes needed to make a new short directory
    def createShortDir(dirName, cluster):
        #dirName = dirName.upper()
        dirNameSplit = dirName.split('.')
        voreName = bytearray(dirNameSplit[0],'utf-8')
        nachName = bytearray(dirNameSplit[1],'utf-8')
        s = ' '
        fullEntry = voreName + bytearray(s *(11-len(dirNameSplit[0])-len(dirNameSplit[1])), 'utf-8') + nachName
        attr = [0x20,0x00,0x00] #archive flag and reseseved bit and CrtTimeTenth
        fullEntry += bytearray(attr)
        fullEntry += getTime() #create time
        fullEntry += getDate() #create Date
        fullEntry += getDate() #access date
        clusterLO = convertLE(cluster & 0xff, 2)
        clusterHI = convertLE(cluster >> 8 , 2)
        fullEntry += clusterHI
        fullEntry += getTime() #write time
        fullEntry += getDate() #write Date
        fullEntry += clusterLO #low cluster word
        fullEntry += convertLE(0,4) #file size (init at 0)

        return fullEntry

        

