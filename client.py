import socket
import sys
import time
import threading
import json
from protocol import *
import datetime
from option import *

# CONNECT TO SERVER
def connect():
    global client
    global connected
    reconnect = True
    while reconnect:
        server_ip = 'localhost'
        server_port = 1111
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
            recv_msg = json.loads(recv_msg)
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
            send_msg = json.dumps({'mode': mode, 'client_id': client_id})
            client.sendall(send_msg.encode())
            login_mode = True
            while login_mode:
                if recv_msg['logined'] == True:
                    print('Login success')
                    print('Welcome', recv_msg['id'])
                    while recv_msg['logined']:
                        mode = input('Enter mode(send, request): ')
                        if mode == 'send':
                            sending = True
                            while sending:
                                receiver_id = input('Enter receiver ID: ')
                                message = input('Enter message: ')
                                send_msg = json.dumps({'mode': mode, 'client_id': client_id, 'receiver_id': receiver_id, 'message': message})
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
                                send_msg = json.dumps({'mode': mode, 'client_id': client_id})
                                client.sendall(send_msg.encode())
                                if recv_msg['requested'] == True:
                                    print('Request success')
                                    print('Messages from', recv_msg['id'])
                                    print(recv_msg['messages'])
                                else:
                                    print('Request failed')
                                requesting = convert_yesno_to_bool(input('Do you want to request again? (y/n): '))
                elif recv_msg['logined'] == False:
                    print('Login failed')
                    login_mode = convert_yesno_to_bool(input('Do you want to login again? (y/n): '))
                            
        elif mode == 'register':
            client_id = input('Enter your ID: ')
            send_msg = {'mode': mode, 'id': client_id}
            client.sendall(send_msg.encode())
            register_mode = True
            while register_mode:
                if recv_msg['registered'] == True:
                    print('Register success')
                    print('Welcome', recv_msg['id'])
                    register_mode = False
                if recv_msg['registered'] == False:
                    print('Register failed')
                    print('ID already exist')
                    register_mode = convert_yesno_to_bool(input('Do you want to register again? (y/n): '))
            continue
        elif mode == 'exit':
            print('Goodbye')
            sys.exit()
        else:
            print('Invalid mode')
            continue

# THREADING
connect()
recv_t = threading.Thread(target=receive)
recv_t.start()
send_t = threading.Thread(target=send)
send_t.start()