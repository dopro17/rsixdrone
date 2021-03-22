#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 17:20:43 2021

@author: douglas
"""
import pygame
import time
import socket
import struct


UDP_IP = "192.168.2.157"
UDP_PORT = 5001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()


packer = struct.Struct('f f')
exios = (0,0)
print ("Inicializando controle!\n\n\n")
try:
    while True:
        event = pygame.event.get()
        pygame.event.clear()
        eixos = (j.get_axis(0), j.get_axis(1))
        print("\rEixo X: %+0.2f Eixo Y: %+0.2f" % eixos, end='')
        packet_data = packer.pack(*eixos)
        
        sock.sendto(packet_data,(UDP_IP, UDP_PORT))
        time.sleep(0.05)

except KeyboardInterrupt:
    print("EXITING NOW")
    j.quit()
    sock.close()
    
    