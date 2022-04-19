from DataLevel import Sector


#class to handle the acual data implementation (read and write lines)
class Data:
    def __init__(self, startSector,Disk):
        self.Disk = Disk
        self.bytesOccupied = 0
        self.Sector = Sector(startSector,Disk)

        self.sectorsOccupied = 0
    
    #function for writing data to a sector. 0 indicates that write was successful > 0 returns the amount of bytes not written due to cluster overflow
    def writeDat(self, bData):
        #if the bytes are smaller than the bytes left on the sector
        if len(bData) <= 512-self.bytesOccupied:
            #simply write the entire array into memory
            self.Sector.writeBytes(self.bytesOccupied,bData,len(bData))
            self.bytesOccupied += len(bData)
            return 0
        else:
            #is there any space left on this sector
            if self.bytesOccupied == 512:
                #is there another sector avalible?
                if self.sectorsOccupied == 4:
                    return len(bData)
                #if not move on to the next sector and recall function
                else:
                    self.Sector.next()
                    self.sectorsOccupied += 1
                    self.bytesOccupied = 0
                    self.writeDat(bData)
            #funky wunky case where theres space on the sector but not enough for the data
            else:
                #chop up bData
                toWrite = bData[0:(512-bytesOccupied)]
                toRecall = bData[(512-bytesOccupied):len(bData)]
                self.Sector.writeBytes(bytesOccupied,toWrite,(512-bytesOccupied))
                self.writeDat(toRecall)
