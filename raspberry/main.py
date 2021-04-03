#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 22:34:12 2021

@author: douglas
"""

import sys
sys.path.append('/opt/drone')
from rsix import *
from pythontimers import *
import _thread, struct, socket



a = 2.4450E-4
b = -3.1758
offset = -0.1
kp = 1.4
ki = 0.15
kd = 0.05
dt = 0.05

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = socket.getaddrinfo('0.0.0.0', 10000)[0][-1]
sock.bind(server)
sock.listen(1)


sr_enc = linear_encoder(adc.CH_A, a, b)
sr_motor = motor(pwm.I2C_PWM2, pwm.I2C_PWM3)
sr_pid = PIDController(kp, ki, kd, dt)
sr = servo(sr_motor, sr_enc, sr_pid, offset)

timer0 = Timer(dt, sr.loop)
timer0.start()

trac = motor(pwm.I2C_PWM0, pwm.I2C_PWM1)

def mainTh():
    buffer = [float()]*5
        
    t_filter = modafilter(5)
    
    
    while True:
        connection, client_addr = sock.accept()
        print("Connection from: %s" % client_addr[0])
        #Allocating data and val before loop avoid dinamica alocation ans speed uo the loop execution "I belive"
        data = bytearray(20)
        val = (float(),)*5
        

        while True:
            try:
                
                nbytes = connection.recv_into(data, 20)
                
                if nbytes:
                    
                    val = struct.unpack('fffff', data)
                    
                    s = t_filter.moda(-val[1])
                    
                    trac.speed(s)
                    sr.position(val[0])
                    print(val)
                
                #need to call sendall() otherwise OSError wont work if connection lost
                connection.sendall(data)                
                    
            except OSError:
                
                trac.speed(0)
                sr.position(0)
                print("Lost control connection")
                connection.close()
                break
try:            
    _thread.start_new_thread(mainTh, ())
except:
    print("Exiting")
    sr_motor.deinit()
    sr_enc.deinit()
    trac.deinit()
    sock.close()
    exit()

