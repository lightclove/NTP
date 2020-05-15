# -*- coding: utf-8 -*-
#!/usr/bin/env python2
########################################################################################################################
# Имя модуля: UDP_Server.py
# Назначение: Сервер прослушивающий порт на наличие дэйтаграмм
# Версия интерпретатора: 2.7.15
# Автор: Дмитрий Ильюшкò ilyushko@itain.ru dm.ilyushko@gmail.com
# Создан: 15.04.2019
# Изменен:
# Лицензия: MIT www.opensource.org/licenses/mit-license.php
########################################################################################################################
import ConfigParser
import datetime
import os
import socket
########################################################################################################################
def init(portIPTuple):
    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
     # Bind to address and ip

    UDPServerSocket.bind((portIPTuple[0], int(portIPTuple[1])))
    print(cur_time() +" UDP server up and listening on ip: " + str(portIPTuple[0]) + " and port: " + str(str(portIPTuple[1])))
    return UDPServerSocket
########################################################################################################################

def serve(socket):
    while (True):
        # Слушаем входящие дэйтаграммы
        # int(config()[2]) - это buffersize из конфиг файла UDP_Client.conf
        bytesAddressPair = socket.recvfrom(int(config()[2]))

        if not bytesAddressPair:
            cur_time() + " Error in bytesAddressPair"
            break
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        clientMsg = cur_time() +" Message from Client: {}".format(message)
        clientIP = cur_time() +" Client IP Address: {}".format(address[0])
        print(clientMsg)
        print(clientIP)

    socket.close()
########################################################################################################################
# Считываем конфиг и его параметры, метод возвращает кортеж из параметров конфига
def config():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_PATH = os.path.join(ROOT_DIR, "UDP_Server.conf")
    config = ConfigParser.ConfigParser()
    config.read(CONFIG_PATH)
    serverAddress = config.get("server", "serverAddress")
    serverPort = config.get("server", "serverPort")
    bufferSize = config.get("server", "bufferSize")
    #print cur_time() +" Config has been read: \"" + str(CONFIG_PATH) +"\""
    return (serverAddress, serverPort, bufferSize)
########################################################################################################################

def cur_time():
     return str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S: "))
########################################################################################################################

if __name__ == '__main__':

    serve(init((config())))
    print
########################################################################################################################