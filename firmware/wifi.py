# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 10:23:51 2021

@author: douglas
"""
import network
from time import sleep

essid = "prodocimo_net"
password = "#prodocimo@net#"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

n=0

while not wlan.isconnected():

    print("Connecting to wifi %s" % essid)
    wlan.connect(essid, password)
    sleep(10)
    wlan.ifconfig()
    n += 1
    if n == 3:
        print("Failed to connect do wifi after 3 times.")
        break
