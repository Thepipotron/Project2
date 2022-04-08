
#include <wiringPiI2C.h>
#include <iostream>
#include <unistd.h>

#define CTRL_REG1 0x20
#define CTRL_REG2 0x21
#define CTRL_REG3 0x22 
#define CTRL_REG4 0x23

#define X 0x0
#define Y 0x1
#define Z 0x2

#define OUT_X_L 0x28
#define OUT_X_H 0x29
#define OUT_Y_L 0x2A
#define OUT_Y_H 0x2B
#define OUT_Z_L 0x2C
#define OUT_Z_H 0x2D

#define SCALE 8

//initialize the Magnetometer given the address of the devic
int MAG_init(int addr){
    int device = wiringPiI2CSetup(addr);

    //power on the device
    wiringPiI2CWriteReg8(device, CTRL_REG3, 0b00000000);

    //set scale to 8 gauss
    wiringPiI2CWriteReg8(device, CTRL_REG2, 0b00100000);

    //set X and Y to medium performance
    wiringPiI2CWriteReg8(device, CTRL_REG1, 0b00110000);

    //set Z to medium performance
    wiringPiI2CWriteReg8(device,CTRL_REG4, 0b00000100);

    return device;
}

//get output of the magnetometer with a given direction
int16_t getMagDir(int dir, int MAG){
    int16_t magDir = wiringPiI2CReadReg8(MAG, (OUT_X_L + (2*dir))) | (wiringPiI2CReadReg8(MAG,OUT_X_L+(2*dir)) << 8);
    return magDir;
}

//get outputs in all three direction. Returned as MagX,MagY,MagZ
double * getMAGCombined(int MAG){

    static double magDat[3];

    for(int i=0; i < 3; i++){
        magDat[i] = double(getMagDir(i,MAG))/INT16_MAX * SCALE;
    }

    return magDat;
}

//test function
/*int main(){
    int MAG = MAG_init(0x1c);

    std::cout.unsetf(std::ios::floatfield);
    std::cout.precision(4);

    while(1){
        //lets do a quick test and make sure its working
        double *Output = getMAGCombined(MAG);

        for(int i = 0; i < 3; i++){
            std::cout<<"\t"<<Output[i];
        }

        std::cout<<std::endl;
    }
    return 0;
}*/