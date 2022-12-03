import socket
import selectors
import sys
import time
import threading
import json
import datetime
from option import *

# CONNECT TO SERVER
def connect():
    global client
    global connected
    reconnect = True
    while reconnect:
        server_ip = '172.17.0.158'
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
        
class appFSM():
    def __init__(self) -> None:
        self.information = {}
        self.socket = connect()
        self.currentMode = loginPhase(self.socket,self.information)
    def main(self):
        while True:
            nextMode = self.currentMode.task()
            if nextMode == None:
                exit()
            self.currentMode = nextMode
            
class loginPhase():
    def __init__(self, socket, information) -> None:
        self.socket = socket
        self.information = information #loginphase does not need information
    def task(self):
        isValidMode = False
        mode = ''
        while not isValidMode:
            mode = input('Enter mode(login, register, exit): ')
            match mode:
                case 'login':
                    return loginMode(self.socket, self.information)
                case 'register':
                    return registerMode(self.socket, self.information)
                case 'exit':
                    return None
                case other :
                    isValidMode = False
class loginMode():
    def __init__(self, socket, information) -> None:
        self.socket = socket
        self.information =information
        self.isLogged = False
        self.sel = selectors.DefaultSelector()
    def task(self):
        self.sel.register(self.socket, selectors.EVENT_WRITE, self.tryLogin)
        while not self.isLogged:
            events = self.sel.select()
            for key, mask in events:
                callback = key.data
                callback()
    def tryLogin(self):
        self.sel.unregister(self.socket)
        client_id = input('Enter your ID: ')
        send_msg = json.dumps({'mode': 'login', 'client_id': client_id})
        self.socket.sendall(send_msg.encode())
        self.tryID = client_id
        self.sel.register(self.socket, selectors.EVENT_READ, self.loginVerify)
    def loginVerify(self):
        self.sel.unregister(self.socket)
        recv_msg = client.recv(1024).decode('utf-8')
        if not recv_msg :
            return
        recv_msg = json.loads(recv_msg)
        if(recv_msg['logined']):
            self.loginSuccess()
        else:
            self.loginFailed()
    def loginFailed(self):
        print("Login Failed\n")
        print("Please Check your ID")
        self.sel.register(self.socket, selectors.EVENT_WRITE, self.tryLogin)
    def loginSuccess(self):
        print("Login by ID : " + self.tryID)
        self.information["Client_ID"] = self.tryID
        self.isLogged = True
class registerMode():
    def __init__(self, socket, information) -> None:
        self.socket = socket
        self.information = information
        self.isRegistered = False
        self.sel = selectors.DefaultSelector()
    def task(self):
        self.sel.register(self.socket, selectors.EVENT_WRITE, self.tryRegister)
        while not self.isRegistered:
            events = self.sel.select()
            for key, mask in events:
                callback = key.data
                callback()
    def tryRegister(self):
        self.sel.unregister(self.socket)
        client_id = input('Enter your ID: ')
        send_msg = json.dumps({'mode': 'register', 'client_id': client_id})
        self.socket.sendall(send_msg.encode())
        self.tryID = client_id
        self.sel.register(self.socket, selectors.EVENT_READ, self.registerVerify)
    def registerVerify(self):
        self.sel.unregister(self.socket)
        recv_msg = client.recv(1024).decode('utf-8')
        if not recv_msg :
            return
        recv_msg = json.loads(recv_msg)
        if(recv_msg['registered']):
            self.registerSuccess()
        else:
            self.registerFailed()
    def registerFailed(self):
        print("Register Failed\n")
        print("Please Check your ID")
        self.sel.register(self.socket, selectors.EVENT_WRITE, self.tryRegister)
    def registerSuccess(self):
        print("Register by ID : " + self.tryID)
        self.isRegistered = True
        self.sel.register(self.socket, selectors.EVENT_WRITE, loginMode(self.socket, self.information))
        
class chattingPhase():
    def __init__(self, socket, information):
        self.socket = socket
        self.information = information
    def task(self):
        isValidMode = False
        while not isValidMode:
            mode = input('Enter mode(send, receive, exit): ')
            match mode:
                case 'send':
                    return sendMode(self.socket, self.information)
                case 'receive':
                    return receiveMode(self.socket, self.information)
                case 'exit':
                    return None
                case other :
                    isValidMode = False
    
# send message to server
class sendMode():
    def __init__(self, socket, information): 
        self.socket = socket
        self.information = information
        self.isChatting = False
        self.sel = selectors.DefaultSelector()
    def task(self):
        self.sel.register(self.socket, selectors.EVENT_WRITE, self.tryChat)
        while not self.isChatting:
            events = self.sel.select()
            for key, mask in events:
                callback = key.data
                callback()
    def trySend(self):
        self.sel.unregister(self.socket)
        receiver_id = input('Enter receiver ID: ')
        message = input('Enter message: ')
        send_msg = json.dumps({'mode': 'send', 'client_id': self.information['Client_ID'], 'receiver_id': receiver_id, 'message': message})
        self.socket.sendall(send_msg.encode())
        self.sel.register(self.socket, selectors.EVENT_READ, self.sendVerify)
    def sendVerify(self):
        self.sel.unregister(self.socket)
        recv_msg = client.recv(1024).decode('utf-8')
        if not recv_msg :
            return
        recv_msg = json.loads(recv_msg)
        if(recv_msg['sent']):
            self.sendSuccess()
        else:
            self.sendFailed()
    def sendFailed(self):
        print("Send Failed\n")
        print("Please Check receiver ID")
        self.sel.register(self.socket, selectors.EVENT_WRITE, self.trySend)
    def sendSuccess(self):
        print("Send Success\n")
        self.isChatting = convert_yesno_to_bool(input('Do you want to send more message? (y/n): '))
        if self.isChatting:
            self.sel.register(self.socket, selectors.EVENT_WRITE, self.trySend)
            
# receive message from server
class receiveMode():
    def __init__(self, socket, information): 
        self.socket = socket
        self.information = information
        self.sel = selectors.DefaultSelector()
    def task(self):
        self.sel.register(self.socket, selectors.EVENT_READ, self.tryReceive)
        while not self.isChatting:
            events = self.sel.select()
            for key, mask in events:
                callback = key.data
                callback()
    def requestMode(self):
        self.sel.unregister(self.socket)
        date = agotime(int(input('Enter days ago number (ex. 1 = yesterday message): '))) # time format : 'YYYY-MM-DD' --> string
        send_msg = json.dumps({'mode': 'request', 'client_id': self.information['Client_ID'], 'date': date})
        self.socket.sendall(send_msg.encode())
        self.sel.register(self.socket, selectors.EVENT_READ, self.receiveVerify)
    def receiveVerify(self):
        self.sel.unregister(self.socket)
        recv_msg = client.recv(1024).decode('utf-8')
        if not recv_msg :
            return
        recv_msg = json.loads(recv_msg)
        if(recv_msg['requested']):
            print("Receive Success\n")
            print(recv_msg['message'])
        else:
            return None

app = appFSM()
app.main()