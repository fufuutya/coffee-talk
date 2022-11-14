import socket
import sys
import time
import threading
import json
from protocol import *

server_ip = 'localhost'
server_port = 1111

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# connect to server
try:
    client_socket.connect((server_ip, server_port))
except:
    print('Connection failed')
    sys.exit()

# receive message from server
def receive():
    while onserver:
        try:
            recv_msg = client_socket.recv(1024).decode()
            if recv_msg == 'exit':  
                break
            print(recv_msg)
            return recv_msg
        except:
            pass
               
            
def convert_yesno_to_bool(yesno):
    if yesno == 'y':
        return True
    elif yesno == 'n':
        return False
    else:
        print('Invalid input')

global onserver
onserver = True
data = clientMode()
def send():
    while onserver:
        global mode
        mode = input('Enter mode(login, register): ')
        sendmore = True
        if mode == 'login':
            client_id = input('Enter your ID: ')
            msg = {'mode': mode, 'id': client_id}
            client_socket.sendall(msg.encode())
            
        elif mode == 'register':
            client_id = input('Enter your ID: ')
            msg = {'mode': mode, 'id': client_id}
            client_socket.sendall(msg.encode())