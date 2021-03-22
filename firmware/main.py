from rsix import *

#Direction servo initialization
sr_motor = motor(25,26)
sr_enc = linear_encoder(36, 1.3793E-3,-2.6814)
sr_pid = PIDController(3.5, 0, 0, 0.1)
sr = servo(sr_motor, sr_enc, sr_pid)
from machine import Timer
tim = Timer(-1)
tim.init(period=100, mode=Timer.PERIODIC, callback=lambda t: sr.loop())
#Direction servo END
