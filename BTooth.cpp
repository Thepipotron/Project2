/*

Bluetooth Module 

Connections

State -------- No Connection
RXD ---------- GPIO15 (UART RX)
TXD ---------- GPIO14 (UART TX)
GND ---------- Ground
VCC ---------- 5V
EN ----------- No Connection


*/
#include <wiringSerial.h>
#include <cstdio>
#include <unistd.h>

int main() {
    int bluetooth  = serialOpen("/dev/ttyS0", 9600);
    if(bluetooth == -1) {
        perror("ERROR\n");
    } else {
        printf("File Descriptor: %d\n", bluetooth);
    }

    serialPuts(bluetooth, "AT\r\n");

    sleep(.1);
    
    int mLength = serialDataAvail(bluetooth);
    if(mLength < 0 ) {
        perror("error\n");
    }

    printf("Length of Message: %d\n", mLength);


    char message[mLength];
   
    for(int i = 0; i++; i < mLength) {
        //message[i] = serialGetchar(bluetooth);
        printf("%c", serialGetchar(bluetooth));
    }
}