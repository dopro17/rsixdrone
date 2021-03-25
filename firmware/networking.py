#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 12:41:34 2021

@author: douglas
"""

"""THI IS A PROTOTYPE LIB I really not sure if this aproach is good or if is
´over procedured`. For while I'm using  manual wifi configuration (but not, I
have a file called wifi.py that is called every boot, but is not in this repo).
"""

class networking:
    def __init__(self, essid, passwd):
        import network
        self.wlan = network.WLAN(network.STA_IF)
        self.essid = essid
        self.passwd = passwd
    
    def start(self, timeout=5):
        from time import sleep
        wlan = self.wlan
        
        print("Starting networking")
        
        if not wlan.isconnected():
            print("Wlan is already connected\n")
            print("Use disconnect before or use restart()")
            return False        
        
        if not wlan.active(True):
            print("Fail to active wlan")
            return False
        
        try:
            wlan.connect(self.essid, self.passwd)
            sleep(timeout)
            
            if wlan.isconnected():
                print("Connected: ", wlan.ifconfig())
                return True
            else:
                print("Could not connect to %s.\n Check essid and passwaord")
                return False
                
        except OSError as e:
            print("Wlan error: ", e)
            return False
        
    
    def restart(self):
        wlan = self.wlan
        
        if not wlan.active(False):
            print("Could not deactive wlan")
            return False
        
        return self.start()
    
    def disconnect(self):
        wlan = self.wlan
        if not wlan.active(False):
            print("Could not deactive wlan")
            return False
        return True
    
    def status(self, signal=False):
        if signal:
            return self.wlan.status('rssi')
        else:
            return self.wlan.status()
    
    
def startnetworking(net_obj):
    import _thread
    from time import sleep
    loop_time = 3
    
    def netloopTh():
        while True:
            status = net_obj.status()
            
            if status == 1001:
                print("Lost network connection")
                net_obj.start()
            
            sleep(loop_time)
    
    th = _thread.start_new_thread(netloopTh,[])
            
        
        
        
        
        
        
        