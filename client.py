import socket
import selectors
import sys
import time
import threading
import json
from protocol import *
import datetime
from option import *

def connect():
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
        except :
            print('Connection failed')
            reconnect = convert_yesno_to_bool(input('Do you want to reconnect? (y/n): '))
            if reconnect == False:
                print('Goodbye')
                sys.exit()
    return client

# RECEIVE FROM SERVER
def receive(connected, client):
    global recv_msg
    while connected:
        try:
            recv_msg = client.recv(1024).decode('utf-8')
            recv_msg = json.loads(recv_msg)
        except:
            print('Connection lost from server')
            break
class appFSM():
    def __init__(self) -> None:
        self.information = {};
        self.socket = connect();
        self.currentMode = loginPhase(self.socket,self.information);
    def main(self):
        while True:
            nextMode = self.currentMode.task();
            if nextMode == None:
                exit();
            self.currentMode = nextMode;
class loginPhase():
    def __init__(self, socket, information) -> None:
        self.socket = socket;
        self.information = information; #loginphase does not need information
    def task(self):
        isValidMode = False;
        mode = '';
        while not isValidMode:
            mode = input('Enter mode(login, register, exit): ')
            match mode:
                case 'login':
                    return loginMode(self.socket, self.information);
                case 'register':
                    return registerMode(self.socket, self.information);
                case 'exit':
                    return None;
                case other :
                    isValidMode = False;
class loginMode():
    def __init__(self, socket, information) -> None:
        self.socket = socket;
        self.information =information;
        self.isLogged = False;
        self.readSel = selectors.DefaultSelector();
        self.writeSel = selectors.DefaultSelector();
    def task(self):
        self.tryLogin();
        self.readSel.register(self.socket, selectors.EVENT_READ, self.loginVerify)
        self.writeSel.register(self.socket, selectors.EVENT_WRITE, self.emptyFunction)
        while not self.isLogged:
            events = self.readSel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj);
            events = self.writeSel.select()
            for key, mask in events:
                callback = key.data;
                callback(key.fileobj);
    def emptyFunction(self, conn):
        pass
    def tryLogin(self):
        client_id = input('Enter your ID: ')
        send_msg = json.dumps({'mode': 'login', 'client_id': client_id})
        self.socket.sendall(send_msg.encode())
        self.tryID = client_id;
    def loginVerify(self, socket):
        self.readSel.unregister(self.socket);
        recv_msg = socket.recv(1024).decode('utf-8')
        if not recv_msg :
            return
        recv_msg = json.loads(recv_msg)
        if(recv_msg['logined']):
            self.loginSuccess();
        else:
            self.loginFailed();
    def loginFailed(self):
        print("Login Failed\n");
        print("Please Check your ID");
        self.sel.register(self.socket, selectors.EVENT_WRITE, self.tryLogin);
    def loginSuccess(self):
        print("Login by ID : " + self.tryID);
        self.information["Client_ID"] = self.tryID;
        self.isLogged = True;
class registerMode():
    def __init__(self) -> None:
        pass
    def task(self):
        pass
class sendingMode():
    def task(self, socket, information):
        pass
#         pass
# def send():
#     global mode
#     global send_msg
#     global client_id
#     while connected:
#         mode = input('Enter mode(login, register, exit): ')
#         if mode == 'login':
#             client_id = input('Enter your ID: ')
#             send_msg = json.dumps({'mode': mode, 'client_id': client_id})
#             client.sendall(send_msg.encode())
#             login_mode = True
#             while login_mode:
#                 if recv_msg['logined'] == True:
#                     print('Login success')
#                     print('Welcome', recv_msg['id'])
#                     while recv_msg['logined']:
#                         mode = input('Enter mode(send, request): ')
#                         if mode == 'send':
#                             sending = True
#                             while sending:
#                                 receiver_id = input('Enter receiver ID: ')
#                                 message = input('Enter message: ')
#                                 send_msg = json.dumps({'mode': mode, 'client_id': client_id, 'receiver_id': receiver_id, 'message': message})
#                                 client.sendall(send_msg.encode())
#                                 if recv_msg['sent'] == True:
#                                     print('Message sent')
#                                 else:
#                                     print('Message not sent due to invalid receiver ID')
#                                     sending = convert_yesno_to_bool(input('Do you want to send message again? (y/n): '))
#                                 sending = convert_yesno_to_bool(input('Do you want to send another message? (y/n): '))
#                         elif mode == 'request':
#                             requesting = True
#                             while requesting:
#                                 send_msg = json.dumps({'mode': mode, 'client_id': client_id})
#                                 client.sendall(send_msg.encode())
#                                 if recv_msg['requested'] == True:
#                                     print('Request success')
#                                     print('Messages from', recv_msg['id'])
#                                     print(recv_msg['messages'])
#                                 else:
#                                     print('Request failed')
#                                 requesting = convert_yesno_to_bool(input('Do you want to request again? (y/n): '))
#                 elif recv_msg['logined'] == False:
#                     print('Login failed')
#                     login_mode = convert_yesno_to_bool(input('Do you want to login again? (y/n): '))
                            
#         elif mode == 'register':
#             client_id = input('Enter your ID: ')
#             send_msg = {'mode': mode, 'id': client_id}
#             client.sendall(send_msg.encode())
#             register_mode = True
#             while register_mode:
#                 if recv_msg['registered'] == True:
#                     print('Register success')
#                     print('Welcome', recv_msg['id'])
#                     register_mode = False
#                 if recv_msg['registered'] == False:
#                     print('Register failed')
#                     print('ID already exist')
#                     register_mode = convert_yesno_to_bool(input('Do you want to register again? (y/n): '))
#             continue
#         elif mode == 'exit':
#             print('Goodbye')
#             sys.exit()
#         else:
#             print('Invalid mode')
#             continue
app = appFSM()
app.main();