
#include <wiringPiI2C.h>
#include <iostream>
#include <unistd.h>

#define CTRL1_XL 0x10
#define CTRL2_G 0x11

#define CTRL5_C 0X14

#define OUTX_L_G 0x22
#define OUTX_H_G 0x23
#define OUTY_L_G 0x24
#define OUTY_H_G 0x25
#define OUTZ_L_G 0x26
#define OUTZ_H_G 0x27

#define OUTX_L_XL 0x28
#define OUTX_H_XL 0x29
#define OUTY_L_XL 0x2A
#define OUTY_H_XL 0x2B
#define OUTZ_L_XL 0x2C
#define OUTZ_H_XL 0x2D

#define X 0x0
#define Y 0x1
#define Z 0x2

#define G_SCALE 245
#define X_SCALE 2

//initialized the IMU device depending on the address of the IMU
int IMU_init(int addr){
    //set up the I2C device
    int device = wiringPiI2CSetup(addr);

    //activate the accelorometer 
    wiringPiI2CWriteReg8(device, CTRL1_XL, 0x50);

    //activate the gyro
    wiringPiI2CWriteReg8(device, CTRL2_G, 0x50);

    //return int for the device
    return device;
}

//returns the output of the accelerometer with the given direction
int16_t getAccDir(int dir, int IMU){
    int16_t accDir = wiringPiI2CReadReg8(IMU, (OUTX_L_XL + (2*dir))) | (wiringPiI2CReadReg8(IMU,OUTX_H_XL+(2*dir)) << 8);
    return accDir;
}

//returns the output of the gyro with the given direction
int16_t getGyroDir(int dir, int IMU){
    int16_t gyroDir = wiringPiI2CReadReg8(IMU, (OUTX_L_G + (2*dir))) | (wiringPiI2CReadReg8(IMU,OUTX_H_G+(2*dir)) << 8);
    return gyroDir;
}

//returns all IMU data in the order AccX, AccY, AccZ, GyroX, GyroY, GyroZ
double * getIMUCombined(int IMU){
    static double imuDat[6];
    
    //iterate through each of the directions
    for(int i = 0; i < 3; i++){
        imuDat[i] = double(getAccDir(i,IMU))/INT16_MAX * X_SCALE;
        imuDat[i+3] = double(getGyroDir(i,IMU))/INT16_MAX * G_SCALE;
    }

    return imuDat;
}

int main(){
    
    int IMU = IMU_init(0x6a);

    std::cout.unsetf(std::ios::floatfield);
    std::cout.precision(4);

    while(1){
        //lets do a quick test and make sure its working
        double *Output = getIMUCombined(IMU);

        for(int i = 0; i < 6; i++){
            std::cout<<"\t"<<Output[i];
        }

        std::cout<<std::endl;
    }
    return 0;
}