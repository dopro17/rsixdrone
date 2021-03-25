#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 17:20:43 2021

@author: douglas
"""
import pygame
import time
import struct
import psutil, os
import signal


p = psutil.Process(os.getpid())
p.nice(10)

print ("Inicializando controle!\n\n\n")
pygame.init()
j = pygame.joystick.Joystick(0)
j.init()

packer = struct.Struct('fffff')


def initconnection(IP, port):
    import socket
    print("Connecting to %s:%d" % (IP, port))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (IP, port)
    sock.connect(server_address)
    
    return sock

    

while True:
    try:
        sock = initconnection('192.168.2.157', 10000)

        while True:

            try:
                event = pygame.event.get()
                pygame.event.clear()
                eixos = (j.get_axis(3), j.get_axis(1),0,0,0)
                
                if eixos[1] < 0.1 and eixos[1] > -0.1:
                
                    eixos = (eixos[0], 0.0,0,0,0)
                   
                sock.send(packer.pack(*eixos))
                reply = sock.recv(20)
                print(struct.unpack('fffff', reply))
                
                time.sleep(0.04)
            
            except OSError:
                print("Lost control connection")
                break
            
            except RuntimeError as e:
                
                print(e)
                break
        
            except KeyboardInterrupt:
                print("Exiting")
                signal.SIGKILL
                break
                
    
    except Exception as e:
        print("Can not connect to server!", e)
        print("retreiving!")

    
    except KeyboardInterrupt:
            print("EXITING NOW")
            j.quit()
            break
    
    

