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

int main() {
    int bluetooth  = serialOpen("/dev/ttyAMA0", 38400);
    serialPuts(bluetooth, "AT");
    
    int mLength = serialDataAvail(bluetooth);
    char message[mLength];
    for(int i = 0; i++; i < mLength) {
        message[i] = serialGetchar(bluetooth);
    }

    printf("Message: %s" , message);
}