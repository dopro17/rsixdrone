# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 13:04:27 2021

@author: douglas prodocimo
"""

class motor:
    def __init__(self, pin_A, pin_B, freq=1000, name=""):
        
        from machine import Pin, PWM
        
        self.output_A = PWM(Pin(pin_A), freq=freq, duty=0)
        self.output_B = PWM(Pin(pin_B), freq=freq, duty=0)
        self.name = name
    
    def speed(self, s):
        
        if (s < -1 and s > 1):
            print("%s : Speed is out of range")
            return None
        
        if (s > 0):
            duty = int(s*1023)
            self.output_B.duty(0)      #Garantir que o dutty seja 0 para evitar curto circuito na ponte
            self.output_A.duty(duty)
            return 1
        
        if (s < 0):
            duty = int(abs(s)*1023)
            self.output_B.duty(duty) 
            self.output_A.duty(0)     #Garantir que o dutty seja 0 para evitar curto circuito na ponte
            return 1
        
        if (s == 0):
            self.output_B.duty(0)
            self.output_A.duty(0)
            return 1
        
    def deinit(self):

        self.output_B.deinit()
        self.output_A.deinit()
        


class linear_encoder:

        def __init__(self, adc_pin, a, b):

            from machine import ADC, Pin
            
            self.a = a
            self.b = b
            self.adc_in = ADC(Pin(adc_pin))
            self.adc_in.atten(ADC.ATTN_11DB)
            self.adc_in.width(ADC.WIDTH_12BIT)
        
        def read(self):
            x = self.adc_in.read()
            y = self.a * x + self.b
            return y



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

    def __init__ (self, motor_obj, encoder_obj, pid_obj, debug=False):

        import _thread
        from machine import Timer
        self.setpoint = 0
        self.setpoint_lock = _thread.allocate_lock()
        self.actual = 0
        self.motor = motor_obj
        self.enc = encoder_obj
        self.pid = pid_obj
        self.block = _thread.allocate_lock()
        self.loop_lock = _thread.allocate_lock()
        self.tim = Timer(-1)
        self.debug = debug
        
        if debug:
            self.data = [float()]*100
            self.n = 0
    
    def debugreset(self):
        if self.debug:
            self.data = [float(), float()]*100
            self.n = 0
        else:
            print("Debug is not enabled")
            
    
    def loop(self):
        
        position = self.enc.read()
        
        if self.setpoint_lock.acquire():
            self.actual = self.setpoint
            self.setpoint_lock.release()
        
        m = self.pid.process(self.setpoint, position)
        self.motor.speed(m)
        
        if self.debug:
            if self.n <= 99:
                self.data[self.n] = [self.setpoint, position]
                self.n += 1
            
        
        
    
    def position(self,p=None):
        if p==None:
            return self.enc.read()

        if self.setpoint_lock.acquire():
            self.setpoint = p
            self.setpoint_lock.release()
        return p            

        
            
        
        
