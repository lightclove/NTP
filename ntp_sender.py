import datetime
import signal
import struct
import time
from contextlib import closing
from socket import socket, AF_INET, SOCK_DGRAM
import threading
import copy
import os
import sys
from ntp_main_client import NTPPacket
from readConfig import read_Config


def time_sender_udp(host='127.0.0.1', port=8889):
    """Starts server on host:port,
    takes NTPPacket from client,
    sends NTPPacket back to client with necessary information for synchronize time with client"""

    FORMAT_DIFF = (datetime.date(1970, 1, 1) - datetime.date(1900, 1, 1)).days * 24 * 3600
    packet = NTPPacket()
    answer = NTPPacket()

    with closing(socket(AF_INET, SOCK_DGRAM)) as sock:
        server = (host, port)
        sock.bind(server)
        while True:
            data, client_address = sock.recvfrom(1024)
            receive = time.time() + FORMAT_DIFF
            packet.unpack(data)

            answer.originate = packet.transmit
            answer.receive = receive
            answer.transmit = time.time() + FORMAT_DIFF

            sock.sendto(answer.pack(), client_address)
            print("Sending NTP-packet to {str(client_address)}\nServer Time: {answer.current_time(receive)[1]}")


def main():
     time_sender_udp(read_Config("ntpserver.json")['host'], read_Config("ntpserver.json")['port'])

def sigint_handler(signum, frame):
    print ('CTRL + C Pressed, program is now stopped!')
    #os.abort()
    #raise SystemExit(1)
    #os.kill(os.getpid(),9)
    sys.exit(0)
#signal.signal(signal.SIGTSTP, sigint_handler) # # Реализация прерывания по нажатию CTRL + Z , unix-only
signal.signal(signal.SIGINT, sigint_handler) # # Реализация прерывания по нажатию CTRL + C

if __name__ == '__main__':
    main()
