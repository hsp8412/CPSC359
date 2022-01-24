# Module: MPU6050_reader
# Author: Sipeng He
# Feature: read the data from the sensors of MPU6050, return the data as a list
# Source: MPU6050.py module by MrTijn/Tijndagamer
#         https://github.com/m-rtijn/mpu6050/blob/master/mpu6050/mpu6050.py
#         Released under the MIT License
#         Copyright (c) 2015, 2016, 2017 MrTijn/Tijndagamer
# Date: 2021.11.02

#import smBus class
from smbus import SMBus

#global variables and scale modifier(Default)
#the idea is obtained from MPU6050.py
GRAVITY_MS2 = 9.80665
ACCEL_SCALE_MODIFIER_2G = 16384.0
GYRO_SCALE_MODIFIER_250DEG = 131.0

#function that read the sensors
def read():
    
    #let b1 be an SMBus object
    b1 = SMBus(1)
    #initialization
    b1.write_byte_data(0x68,0x6B,0x00)
    #read the raw value stored in registers 59-72
    L = b1.read_i2c_block_data(0x68, 59, 14)
    
    b1.close()
    
    #concatenate the higher bits and lower bits of each measurement
    #store the raw data of the measurements in a list L_data
    L_data = []
    ACCEL_X_raw = (L[0] << 8) + L[1]
    L_data.append(ACCEL_X_raw)
    ACCEL_Y_raw = (L[2] << 8) + L[3]
    L_data.append(ACCEL_Y_raw)
    ACCEL_Z_raw = (L[4] << 8) + L[5]
    L_data.append(ACCEL_Z_raw)
    Gyro_X_raw = (L[8] << 8) + L[9]
    L_data.append(Gyro_X_raw)
    Gyro_Y_raw = (L[10] << 8) + L[11]
    L_data.append(Gyro_Y_raw)
    Gyro_Z_raw = (L[12] << 8) + L[13]
    L_data.append(Gyro_Z_raw)
            
    #treatment for the negative value obtained in the list
    #the idea is obtained from MPU6050.py
    for x in range(6):
        if(L_data[x] >= 0x8000):
            L_data[x] = -((65535 - L_data[x]) + 1)
            
    #scale the accelerometer measurements
    #the idea is obtained from MPU6050.py
    for x in range(0,3):
        L_data[x] = L_data[x]/ACCEL_SCALE_MODIFIER_2G
        L_data[x] = L_data[x]*GRAVITY_MS2
        
    #scale the gyroscope measurements
    #the idea is obtained from MPU6050.py
    for x in range(3,6):
        L_data[x] = L_data[x]/GYRO_SCALE_MODIFIER_250DEG
    
    return L_data