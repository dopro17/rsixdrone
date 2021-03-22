from rsix import *
from machine import Timer
import socket, struct, _thread

UDP_IP = "192.168.2.157"
UDP_PORT = 5001

sr_motor = motor(25,26, freq=500)
sr_enc = linear_encoder(36, 1.3793E-3,-2.6814)
sr_pid = PIDController(1.4, 0.15, 0.05, 0.05)
sr = servo(sr_motor, sr_enc, sr_pid, debug=True)
tim = Timer(-1)
tim.init(period=50, mode=Timer.PERIODIC, callback=lambda t: sr.loop())

trac = motor(32, 33, freq=100, name="Tracao")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def mainTh():
    while True:
        data, addr = sock.recvfrom(8)
        eixos_v = struct.unpack('ff', data)
        print(eixos_v)
        trac.speed(-eixos_v[1])
        sr.position(eixos_v[0])

th = _thread.start_new_thread(mainTh, [])
