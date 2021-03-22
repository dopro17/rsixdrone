import socket
import struct
import motorcontrol

trac = motorcontrol.motor(32, 33, freq=500, name="Tracao")

UDP_IP = "192.168.2.157"
UDP_PORT = 5001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    
    data, addr = sock.recvfrom(8)
    eixos_v = struct.unpack('ff', data)
    print(eixos_v)
    trac.speed(-eixos_v[0])                                                    #o eixo y é invertido

