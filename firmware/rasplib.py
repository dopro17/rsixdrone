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

    def __init__(self, channel):
        self.file = open(channel, 'r')

    def read(self):
        value = self.file.readline()
        self.file.seek(0)

        return int(value)

    def deinit(self):
        self.file.close()


#%%
class pwm:
    I2C_PWM0 = ('/sys/class/pwm/pwmchip0/', 0, 1000)
    I2C_PWM1 = ('/sys/class/pwm/pwmchip0/', 1, 1000)
    I2C_PWM2 = ('/sys/class/pwm/pwmchip0/', 2, 1000)
    I2C_PWM3 = ('/sys/class/pwm/pwmchip0/', 3, 1000)
    I2C_PWM4 = ('/sys/class/pwm/pwmchip0/', 4, 1000)
    I2C_PWM5 = ('/sys/class/pwm/pwmchip0/', 5, 1000)
    I2C_PWM6 = ('/sys/class/pwm/pwmchip0/', 6, 1000)
    I2C_PWM7 = ('/sys/class/pwm/pwmchip0/', 7, 1000)
    I2C_PWM8 = ('/sys/class/pwm/pwmchip0/', 8, 1000)
    I2C_PWM9 = ('/sys/class/pwm/pwmchip0/', 9, 1000)
    I2C_PWM10 = ('/sys/class/pwm/pwmchip0/', 10, 1000)
    I2C_PWM11 = ('/sys/class/pwm/pwmchip0/', 11, 1000)
    I2C_PWM12 = ('/sys/class/pwm/pwmchip0/', 12, 1000)
    I2C_PWM13 = ('/sys/class/pwm/pwmchip0/', 13, 1000)
    I2C_PWM14 = ('/sys/class/pwm/pwmchip0/', 14, 1000)
    I2C_PWM15 = ('/sys/class/pwm/pwmchip0/', 15, 1000)


    def __init__(self, pwm_ch, freq=1000):
        import os

        self.pwm_ch =  pwm_ch

        #Check if pwmchip is configured and its free (by dtoverlay)
        if not os.path.exists(pwm_ch[0]):
            raise NameError("The path to pwm doesn\'t exists: check if dtoverlay is configured!")

        #Check if channel is free
        if os.path.exists(pwm_ch[0] + "pwm{}".format(pwm_ch[1])):
            raise NameError("The pwm channel {}pwm{} is already initialized!".format(pwm_ch[0],pwm_ch[1]))

        #Check if frequency is in pwm chip range
        if pwm_ch[2] <= freq <= 0:
            self.freq = freq
            self.p = int(1E9/freq)
        else:
            raise NameError("PWM frequency out of range!")

       #Everything looks to be ok! soo...
        try:
            with open(pwm_ch[0] + "export", "w") as f:
                f.write(str(pwm_ch[1]))

            with open(pwm_ch[0] + "pwm{}/period".format(pwm_ch[1]), "w") as f:
                f.write(str(self.p))

            with open(pwm_ch[0] + "pwm{}/enable".format(pwm_ch[1]), "w") as f:
                f.write(str(1))

                self.fdpwm = open(pwm_ch[0] + "pwm{}/duty_cycle".format(pwm_ch[1]), "w")

        except:
            print("Error to initiate PWM channel")

    def duty(self, d):
        if 1 <= d <= 0:
            duty_cycle = int(self.p * d)
    
            self.fdpwm.write(str(duty_cycle))
            self.fdpwm.seek(0)
    #        with open(self.pwm_ch[0] + "pwm{}/duty_cycle".format(pwm_ch[1]), "w") as f:
    #            f.write(str(duty))
            return True

        print("Duty cycle out of range -1 to 1")
        
        return False
        
    def frequency(self, frequency):
        if self.freq <= self.pwm_ch[2] and self.freq >= 0:
            self.freq = frequency
            self.p = int(1E9/frequency)
            with open(self.pwm_ch[0] + "pwm{}/period".format(self.pwm_ch[1]), "w") as f:
                f.write(str(self.p))

            return True

        print("PWM frequency out of range!")

        return False


    def deinit(self):
        self.fdpwm.close()
        with open(self.pwm_ch[0] + "unexport", "w") as f:
            f.write(str(self.pwm_ch[1]))
    
    
        
    
    