#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 13:08:48 2021

@author: douglas
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 19:47:48 2021

@author: douglas
"""

from time import sleep
import camera

camera.init(0, format=camera.JPEG, framesize=camera.FRAME_SVGA)
camera.quality(40)


def server():
    import socket
    import utime
    loop_t = 100
    
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
            start_t = utime.ticks_ms()
            jpg = camera.capture()
            conn.sendall(bund1.format(len(jpg)).encode())
            conn.sendall(jpg + b'\n')
            end_t = utime.ticks_ms()
            t_diff = utime.ticks_diff(end_t, start_t)
            print(t_diff)
            if t_diff > loop_t :
                t_diff = loop_t 
            utime.sleep_ms(loop_t  - t_diff)
        
        except Exception as e:
            print(e)
            break