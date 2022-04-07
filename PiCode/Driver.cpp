//include all written files
#include "IMU.cpp"
#include "MAG.cpp"

#include <unistd.h>

//code to drive the entire operation of the rpi
int main(){

    //initializtion step

    //initialize the IMU
    int IMU = IMU_init(0x6a);

    int MAG = MAG_init(0x1c);

    //setup print format
    std::cout.unsetf(std::ios::floatfield);
    std::cout.precision(4);

    //loop forever
    while(1){
        double *out_imu = getIMUCombined(IMU);
        double *out_mag = getMAGCombined(MAG);

        //create array vals and copy the values of out imu and out mag
        double vals[9];

        for(int i = 0; i < 6; i++){
            test[i] = out_imu[i];
        }
        for(int i = 0; i < 3; i++){
            test[i+6] = out_mag[i];
        }

        //for
        for(int i = 0; i < 9; i++){
            std::cout << "\t" << test[i];
        }

        std::cout<<std::endl;
    }
}