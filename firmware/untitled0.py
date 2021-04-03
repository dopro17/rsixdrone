#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 11:25:43 2021

@author: douglas
"""
#%%
class adc:
    CH_A = '/sys/class/i2c-adapter/i2c-1/1-0048/iio:device0/in_voltage0_raw'
    CH_B = '/sys/class/i2c-adapter/i2c-1/1-0048/iio:device0/in_voltage1_raw'
    CH_C = '/sys/class/i2c-adapter/i2c-1/1-0048/iio:device0/in_voltage2_raw'
    CH_D = '/sys/class/i2c-adapter/i2c-1/1-0048/iio:device0/in_voltage3_raw'
    
    def __init__ (self, channel):
        self.file = open(channel, 'r')
    
    def read(self):
        v = self.file.readline()
        self.file.seek(0)
    
        return int(v)
    
    def deinit(self):
        self.file.close()


    