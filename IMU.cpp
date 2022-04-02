
#include <wiringPiI2C.h>
#include <iostream>
#include <unistd.h>

#define CTRL1_XL 0x10
#define CTRL2_G 0x11

#define CTRL5_C 0X14

#define OUTX_L_G 0x22
#define OUTX_H_G 0x23

#define OUTX_L_XL 0x28
#define OUTX_H_XL 0x29

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




int main(){
    
    int IMU = IMU_init(0x6a);

    while(1){
        //lets do a quick test and make sure its working

        uint8_t ctrl1 = wiringPiI2CReadReg8(IMU,CTRL5_C);

        //std::cout << "Val :" << unsigned(ctrl1) << std::endl;


        //get x accl
        int16_t acc_x = wiringPiI2CReadReg8(IMU, OUTX_L_XL) | (wiringPiI2CReadReg8(IMU,OUTX_H_XL) << 8);;
        
        //get x gyro
        int16_t gyro_x = wiringPiI2CReadReg8(IMU, OUTX_L_G) | (wiringPiI2CReadReg8(IMU,OUTX_H_G) << 8);

        double acc = (double(acc_x)/ INT16_MAX) * 2;
        double gyro = (double(gyro_x) / INT16_MAX) * 245;

        std::cout<<"ACCX: " << acc << " GYROX: " << gyro<<std::endl;
    }
    return 0;
}