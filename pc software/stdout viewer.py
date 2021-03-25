#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 13:54:26 2021

@author: douglas
"""

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = socket.getaddrinfo('0.0.0.0', 10001)[0][-1]
sock.bind(server)
sock.listen(1)

connection, client_addr = sock.accept()
print("Connection from: %s" % client_addr[0])



file = connection.makefile('r')

while True:
    print (file.readline())
