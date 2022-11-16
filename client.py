import socket
import sys
import time
import threading
import json
from protocol import *

# OPTIONAL FUNCTION
def convert_yesno_to_bool(yesno):
    if yesno == 'y':
        return True
    elif yesno == 'n':
        return False
    else:
        print('Invalid input')

# CONNECT TO SERVER
def connect():
    global client
    global connected
    reconnect = True
    while reconnect:
        server_ip = input('Enter server IP: ')
        server_port = input('Enter server port: ')
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            client.connect((server_ip, int(server_port)))
            print('Connected to server')
            reconnect = False
            connected = True
        except:
            print('Connection failed')
            reconnect = convert_yesno_to_bool(input('Do you want to reconnect? (y/n): '))
    if reconnect == False:
        print('Goodbye')
        sys.exit()
    return client

# RECEIVE FROM SERVER
def receive():
    global recv_msg
    while connected:
        try:
            recv_msg = client.recv(1024).decode('utf-8')
        except:
            print('Connection lost from server')
            break
        
def send():
    global mode
    global send_msg
    global client_id
    while connected:
        mode = input('Enter mode(login, register, exit): ')
        if mode == 'login':
            client_id = input('Enter your ID: ')
            send_msg = {'mode': mode, 'id': client_id}
            client.sendall(send_msg.encode())
            if recv_msg['logined'] == True:
                print('Login success')
                print('Welcome', recv_msg['id'])
                while recv_msg['logined']:
                    mode = input('Enter mode(send, request, exit): ')
                    if mode == 'send':
                        sending = True
                        while sending:
                            receiver_id = input('Enter receiver ID: ')
                            message = input('Enter message: ')
                            send_msg = {'mode': mode, 'id': client_id, 'receiver_id': receiver_id, 'message': message}
                            client.sendall(send_msg.encode())
                            if recv_msg['sent'] == True:
                                print('Message sent')
                            else:
                                print('Message not sent due to invalid receiver ID')
                                sending = convert_yesno_to_bool(input('Do you want to send message again? (y/n): '))
                            sending = convert_yesno_to_bool(input('Do you want to send another message? (y/n): '))
                    elif mode == 'request':
                        requesting = True
                        while requesting:
                            send_msg = {'mode': mode, 'id': client_id}
                            client.sendall(send_msg.encode())
                            if recv_msg['requested'] == True:
                                print('Request success')
                                print('Messages from', recv_msg['id'])
                                print(recv_msg['messages'])
                            else:
                                print('Request failed')
                            requesting = convert_yesno_to_bool(input('Do you want to request again? (y/n): '))
                            
        elif mode == 'register':
            client_id = input('Enter your ID: ')
            send_msg = {'mode': mode, 'id': client_id}
            client.sendall(send_msg.encode())
        elif mode == 'exit':
            print('Goodbye')
            sys.exit()
        else:
            print('Invalid mode')
            continue