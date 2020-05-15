# -*- coding: utf-8 -*-
#!/usr/bin/env python2
########################################################################################################################
# Имя модуля: UDP_Client.py
# Назначение: Отсылка дэйтаграмм
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
def cur_time():
     return str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S: "))
########################################################################################################################

# Create a UDP socket at client side
def send(message, serverAddressPort):
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Send to server using created UDP socket
    message = config()[2]
    UDPClientSocket.sendto(message, serverAddressPort)
    print cur_time() + "message: "+message + " sent to ip-address: \""\
          + str(serverAddressPort[0]) + "\", and port: " + str(serverAddressPort[1])
########################################################################################################################
# Считываем конфиг и его параметры, метод возвращает кортеж из параметров конфига
def config():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_PATH = os.path.join(ROOT_DIR, "UDP_Server.conf")
    config = ConfigParser.ConfigParser()
    config.read(CONFIG_PATH)
    serverAddress = config.get("server", "serverAddress")
    serverPort = config.get("server", "serverPort")
    message = config.get("client", "message")

    #print cur_time() +" Config has been read: \"" + str(CONFIG_PATH) +"\""
    return (serverAddress, int(serverPort), message)
########################################################################################################################

if __name__ == '__main__':
    tupleIpPort = ( config()[0], config()[1] )
    send(config()[2], tupleIpPort )
    print
#######################################################################################################################