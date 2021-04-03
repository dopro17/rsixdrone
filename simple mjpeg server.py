#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 19:47:48 2021

@author: douglas
"""

import _thread
from time import sleep

def server():
    import socket
    from time import sleep
    
    jpg = open("/tmp/001.jpg", "rb")
    jpegbuff = jpg.read()
    jpg.close()
    print(len(jpegbuff))
    
    
    header= 'HTTP/1.0 200 OK\n'\
            'Content-type: application/octet-stream\n' \
            'Cache-Control: no-cache\n' \
            'Connection: close\n\n\n' \
            
    
    bund1 = "--boundarydncross\n" \
           "Content-Type: image/jpeg\n" \
           "Content-Length: {}\n\n" \
           


    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("0.0.0.0", 10001))
    sock.listen(1)
    
    conn, client_addr = sock.accept()
    conn.sendall(header.encode())
    

    while True:
        try:
            conn.sendall(bund1.format(len(jpegbuff)).encode())
            conn.sendall(jpegbuff + b'\n')
        
        except Exception as e:
            print(e)
            break
    
    

def client():
    import socket
    
    file = open('/tmp/cap', 'rb')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 10002))

    f = sock.makefile(mode='wb', buffering=0)
    
    while True:
        b = file.read(1)
        if b:
            f.write(b)
        else:
            break
        
    f.close()
    file.close()



    
    
    
    
    