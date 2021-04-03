# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 13:04:27 2021

@author: douglas prodocimo
"""

"""
Port to raspberry pi 3 b+
This lib contains all necessary functions to initialize hardware as objects
like servo control (with PID), traction motor and some simple math filters.
The intent about this lib is to keep the main code clean.
This file is organized from low level to hight level classes, if you want to
read PID code go to end of the file else for read low level stuffs start
reding from here!
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


    def __init__ (self, pwm, freq=1000):
        import os
        
        self.pwm =  pwm

        #Check if pwmchip is configured and its free (by dtoverlay)
        if not os.path.exists(pwm[0]):
            raise NameError("The path to pwm doesn\'t exists: check if dtoverlay is configured!")
        
        #Check if channel is free
        if os.path.exists(pwm[0] + "pwm{}".format(pwm[1])):
            raise NameError("The pwm channel {}pwm{} is already initialized!".format(pwm[0],pwm[1]))
        
        
        #Check if frequency is in pwm chip range
        if freq <= pwm[2] and freq >= 0:
            self.freq = freq
            self.p = int(1E9/freq)
        else:
            raise NameError("PWM frequency out of range!")
        
        #Everything looks to be ok! soo...
#        try:
        with open(pwm[0] + "export", "w") as f:
            f.write(str(pwm[1]))

        with open(pwm[0] + "pwm{}/period".format(pwm[1]), "w") as f:
            f.write(str(self.p))

        with open(pwm[0] + "pwm{}/enable".format(pwm[1]), "w") as f:
            f.write(str(1))
            
            self.fdpwm = open(pwm[0] + "pwm{}/duty_cycle".format(pwm[1]), "w")
            
#        except:
#            print("Error to initiate PWM channel")

    def duty(self, d):
        if 1 >= d >= 0:
            duty = int(self.p * d)
            
            self.fdpwm.write(str(duty))
            self.fdpwm.seek(0)
            
            return True
        
        print("Duty cycle out of range -1 to 1")
        return False



    def freq(self, f):
        if self.freq <= pwm[2] and self.freq >= 0:
            self.freq = f
            self.p = int(1E9/f)
            with open(pwm[0] + "pwm{}/period".format(pwm[1]), "w") as f:
                f.write(str(self.p))

            return True
        else:
            print("PWM frequency out of range!")

            return False


    def deinit(self):
         self.fdpwm.close()
         with open(self.pwm[0] + "unexport", "w") as f:
             f.write(str(self.pwm[1]))
    


class motor:
    def __init__(self, ch0, ch1, freq=1000, name=""):
        
        self.output_A = pwm(ch0)
        self.output_B = pwm(ch1)
        self.name = name
    
    def speed(self, s):
        
        if (s < -1 and s > 1):
            print("%s: Speed is out of range")
            return False
        
        if (s > 0):
            self.output_B.duty(0)      #Garantir que o dutty seja 0 para evitar curto circuito na ponte
            self.output_A.duty(s)
            return True
        
        if (s < 0):
            self.output_B.duty(-s) 
            self.output_A.duty(0)     #Garantir que o dutty seja 0 para evitar curto circuito na ponte
            return True
        
        if (s == 0):
            self.output_B.duty(0)
            self.output_A.duty(0)
            return True
        
    def deinit(self):

        self.output_B.deinit()
        self.output_A.deinit()
        


class linear_encoder:

        def __init__(self, adc_ch, a, b):
            self.a = a
            self.b = b
            self.adc_in = adc(adc_ch)
        
        def read(self):
            x = self.adc_in.read()
            y = self.a * x + self.b
            return y
        
        def deinit(self):
            self.adc_in.deinit()



class PIDController:
    
    def __init__(self, kp, ki, kd, dt, name=""):

        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.name = name
        self.last_e = 0
        
    def process(self, set_point, encoder_value):

        if (encoder_value < -1 and encoder_value > 1):
            print("PID %s: encoder value is out of range -1<= v <= 1" % self.name)
            print("PID %s: shutdown" % self.name)
            output = 0

        if (set_point < -1 and set_point > 1):
            print("PID %s: set point is out of range -1<= v <= 1" % self.name)
            print("PID %s: shutdown" % self.name)
            output = 0

        else:
            e = set_point - encoder_value
            delta_e = e - self.last_e
            output = self.kp*e + self.ki*e*self.dt + self.kd*delta_e/self.dt
            self.last_e = e
            
        if (output < -1):
            print("PID %s: window down value" % self.name)
            output = -1
        
        if (output > 1):
            print("PID %s: windows up value" % self.name)
            output = 1
        
        return output

        

class servo:

    def __init__ (self, motor_obj, encoder_obj, pid_obj, offset):

        import _thread
        self.offset = offset
        self.setpoint = 0
        self.setpoint_lock = _thread.allocate_lock()
        self.actual = 0
        self.motor = motor_obj
        self.enc = encoder_obj
        self.pid = pid_obj
        self.block = _thread.allocate_lock()
        self.loop_lock = _thread.allocate_lock()
#        self.debug = debug #Need to debug=False in __init__ args) 
        
#        if debug:
#            self.data = [float()]*100
#            self.n = 0
    
#    def debugreset(self):
#        if self.debug:
#            self.data = [float(), float()]*100
#            self.n = 0
#        else:
#            print("Debug is not enabled")
            
    
    def loop(self):
        
        position = self.enc.read() + self.offset
        
        if self.setpoint_lock.acquire():
            self.actual = self.setpoint
            self.setpoint_lock.release()
        
        m = self.pid.process(self.actual, position)
        self.motor.speed(m)
        
#        if self.debug:
#            if self.n <= 99:
#                self.data[self.n] = [self.setpoint, position]
#                self.n += 1
            
        
        
    
    def position(self,p=None):
        if p==None:
            return self.enc.read() + self.offset

        if self.setpoint_lock.acquire():
            self.setpoint = p
            self.setpoint_lock.release()
        return p            


#Math lib for control


class modafilter:
    
    def __init__(self, size=5):
        self.size = size
        self.buffer = [float()]*size
        
        
    def moda(self, x):
        self.buffer.pop(-1)
        self.buffer.insert(0, x)
        
        res = 0
        for n in self.buffer:
            res = res + n
    
        return res/self.size