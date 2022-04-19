import adafruit_sdcard
import busio
import board
import digitalio

#read in little endian a raw byte array
def readLEBytes(bArray , offset, count):
    bRes = bytearray(count)
    for c in range(0,count):
        bRes[c] = bArray[offset+c]
    result = int.from_bytes(bRes, "little")
    return result

#read in big endian a raw byte array
def readBEBytes(bArray,offset,count):
    bRes = bytearray(count)
    for c in range(0,count):
        bRes[c] = bArray[offset+c]
    
    result = int.from_bytes(bRes, "big")
    return result


def readBytes(bArray,offset,count):
    bRes = bytearray(count)
    for c in range(0,count):
        bRes[c] = bArray[offset+c]
    
    return bRes

#converts given value (int) into a little endian bytearray
def convertLE(value,count):
    result = value.to_bytes(count, 'little')
    return result

#an extra abstraction to read and write from Sectors
class Sector:
    def __init__(self, sector,disk):
        self.disk = disk
        self.RawBytes = self.disk.read(sector,1) #read one sector from disk
        self.sector = sector
    
    #reads count bytes from the sector and returns as an int returns in LE
    def readLEBytes(self, offset, count):
        bRes = bytearray(count)
        for c in range(0,count):
            bRes[c] = self.RawBytes[offset+c]

        result = int.from_bytes(bRes, "little")
        return result

    def readBEBytes(self,offset,count):
        bRes = bytearray(count)
        for c in range(0,count):
            bRes[c] = self.RawBytes[offset+c]

        result = int.from_bytes(bRes, "big")
        return result
    
    def readBytes(self,offset,count):
        bRes = bytearray(count)
        for c in range(0,count):
            bRes[c] = self.RawBytes[offset+c]

        return bRes

    #writes count bytes in bArray to the SD
    def writeBytes(self,offset,bArray,count):
        if(offset+count > 512):
            print("invalid write spilling over sectors")
        #first get all data before the write
        before = self.readBytes(0,offset)
        #next get bytes after the read
        after = self.readBytes(offset+count, 512-count-offset)

        newBytes = before + bArray + after
        print(newBytes)
        self.disk.write(self.sector,512,newBytes)
        self.RawBytes = self.disk.read(self.sector,1) #read new sector info back from the disk to update rawbytes

    def changeSec(self,sector):
        self.sector = sector
        self.RawBytes = self.disk.read(self.sector,1)

    #moves pointer to the next sector
    def next():
        self.sector += 1
        self.RawBytes = self.disk.read(sector,1)

    


class Disk:
    def __init__(self):
        print("Initializing disk...")
        spi = board.SPI()
        self.sd = adafruit_sdcard.SDCard(spi,  digitalio.DigitalInOut(board.CE0))
    def ioctl_get_sector_count(self):
        return self.sd.count()
    def ioctl_get_sector_size(self):
        return 2048
    def ioctl_get_block_size(self):
        return 1
    def ioctl_sync(self):
        pass
    def ioctl_trim(self):
        pass
    def read(self, sector, count) -> bytes:
        result = bytearray(count*512)
        self.sd.readblocks(sector,result)
        return result
    def write(self, sector, count, buff: bytes):
        print("test")
        buff = bytearray(buff)
        self.sd.writeblocks(sector,buff)

