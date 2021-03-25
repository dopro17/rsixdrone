# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 21:34:56 2021

@author: douglas
"""

from rsix import *
from machine import Timer
import socket, struct, _thread

#Setup the tcp server to receive data from pc host
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = socket.getaddrinfo('0.0.0.0', 10000)[0][-1]
sock.bind(server)
sock.listen(1)

#setup the hardware
sr_motor = motor(25,26, freq=500)
sr_enc = linear_encoder(36, 1.3793E-3,-2.6814)
sr_pid = PIDController(1.4, 0.15, 0.05, 0.05)
sr = servo(sr_motor, sr_enc, sr_pid, debug=True)
tim = Timer(-1)
tim.init(period=50, mode=Timer.PERIODIC, callback=lambda t: sr.loop())

trac = motor(32, 33, freq=100, name="Tracao")
   
        
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
                
                nbytes = connection.readinto(data, 20)
                
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
            
th = _thread.start_new_thread(mainTh, [])

