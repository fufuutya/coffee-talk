import socket
import sys
import time
import threading
import json


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
    while True:
        try:
            # receive message from server
            message = client_socket.recv(1024).decode()
            if message == 'LOGIN_SUCCESS':
                print('Login success')
            elif message == 'REGISTER_SUCCESS':
                print('Register success')
            elif message == 'LOGIN_FAIL':
                print('Login failed')
               
            
def convert_yesno_to_bool(yesno):
    if yesno == 'y':
        return True
    elif yesno == 'n':
        return False
    else:
        print('Invalid input')
# login or register
# def login_session():
#     mode = input('Enter mode(login, register): ')
#     if mode == 'login':
#         client_socket.sendall('LOGIN\\'.encode())
#         client_socket.sendall(input('Enter your ID: ').encode())
#     elif mode == 'register':
#         client_socket.sendall('REGISTER\\'.encode())
#         client_socket.sendall(input('Enter your ID: ').encode())
#     else:
#         print('Invalid mode')
#         sys.exit()

# def enter_chatroom():
#     mode = input('Enter mode(request, send): ')
#     if mode == 'request':
#         client_socket.sendall('REQUEST\\'.encode())
#         client_socket.sendall(input('Enter your ID: ').encode())

onserver = True
def send():
    while onserver:
        mode = input('Enter mode(login, register, request, send): ')
        sendmore = True
        if mode == 'login':
            client_id = input('Enter your ID: ')
            msg = json.dumps({'mode': 'login', 'client_id': client_id})
            client_socket.sendall(msg.encode())
        elif mode == 'register':
            client_id = input('Enter your ID: ')
            msg = json.dumps({'mode': 'register', 'client_id': client_id})
            client_socket.sendall(msg.encode())