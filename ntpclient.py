from ntp_main_client import NTPPacket
import time
import datetime
import socket
from contextlib import closing

from readConfig import read_Config


def time_client_udp(host='127.0.0.1', port=8889):
    """Sends NTPPacket to host:port and checks it's answer"""
    FORMAT_DIFF = (datetime.date(1970, 1, 1) - datetime.date(1900, 1, 1)).days * 24 * 3600
    packet = NTPPacket(version_number=4, mode=3, transmit=time.time() + FORMAT_DIFF)
    answer = NTPPacket()

    with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
        sock.settimeout(5)
        sock.sendto(packet.pack(), (host, port))
        data, server_address = sock.recvfrom(1024)
        arrive = time.time() + FORMAT_DIFF
        answer.unpack(data)
        result = "Time difference: {}\nSynchronize with server time: {}\n".format(*answer.current_time(arrive))
        print(result)

if __name__ == '__main__':
    #time_client_udp()
    time_client_udp(read_Config("ntpclient.json")['host'], read_Config("ntpclient.json")['port'])
