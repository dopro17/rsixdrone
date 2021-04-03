#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 23:25:40 2021

@author: Douglas Drodocimo (github.com/dopro17)
"""

"""
Soft timer object based in time sleep with execution time corrections, can run
more tha one instances. Non blocking, uses a thread to call the callback
function.
"""

class SoftTimer:
    """Retruns a softtimer object"""
    def __init__(self, period, callback, *args):
        import _thread

        self.callback = callback
        self.period = period
        self.args = args
        self.thr = None
        self.kill = _thread.allocate_lock()

    def loop(self):
        """Internal loop do not use it!"""
        from time import clock_gettime
        from time import sleep

        callback = self.callback
        args = self.args
        period = self.period
        kill = self.kill

        t_now = clock_gettime(0)
        t_last = t_now - period

        #Do not call self.(stuff) inside the loop!
        while True:
            t_now = clock_gettime(0)
            delta_t = t_now - t_last
            sleep_t = 2*period - delta_t
            callback(*args)

            sleep(sleep_t)
            t_last = t_now
            if kill.locked():
                break

    def start(self):
        """To start soft timer object."""
        import threading

        self.thr = threading.Thread(target=self.loop)
        self.thr.start()

    def stop(self):
        """To stop soft timer object."""
        self.kill.acquire()
