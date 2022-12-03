import socket
import datetime
import sys
import json
import queue
import select
import protocol
import selectors
from DB import Database

class ClientConnection():
    def __init__(self, clientSocket:socket, database : Database) -> None:
        self.clientSocket = clientSocket;
        self.database : Database = database
        self.isLogged = False;
        self.clientID = None;
        self.OutputQueue = [];
    def acceptPacket(self, conn):
        recv_msg = conn.recv(1024).decode('utf-8');
        recv_msg = json.loads(recv_msg);
        match recv_msg['mode']:
            case 'login':
                self.login(recv_msg['id'])
            case 'registered':
                self.register(recv_msg['id'])
            case 'send':
                self.sendMSG(recv_msg['client_id'],recv_msg['receiver_id'],recv_msg['message'], recv_msg['date'])
            case 'request':
                self.receiveMSG(recv_msg['client_id'], recv_msg['date']);
    def receiveMSG(self, clientID, date):
        if self.isValidClient(clientID):
            data = self.database.getMessageFor(clientID, date);
            for letter in data:
                senderID = letter[0]
                message = letter[2]
                date = letter[3]#need to fix magic number problem.
                send_msg = json.dumps({'mode':'request','requested' : True ,'client_id' : clientID,'sender_id' : senderID, 'message' : message, 'date' : date})
                self.OutputQueue.append(send_msg);
        else:
            send_msg = json.dumps({'mode' : 'request', 'requested' : False, 'client_id' : clientID});
            self.OutputQueue.append(send_msg);
        
            
    def sendMSG(self, senderID, receiverID, msg, date):
        isSent = False;
        if self.isValidClient(senderID):
            self.database.addMessage(senderID, receiverID, msg, date)
            isSent = True;
        else:
            pass
        send_msg = json.dumps({'mode':'send', 'client_id': senderID, 'receiver_id' : receiverID, 'sent' : isSent})
        self.OutputQueue.append(send_msg);
            
    def register(self,ID):
        if self.database.isIDExist(ID):
            self.database.addID(ID);
            self.isLogged = True;
            self.clientID = ID;
        send_msg = json.dumps({'mode':"register", 'registered': self.isLogged});
        self.OutputQueue.append(send_msg);
    def login(self, ID):
        if not self.database.isIDExist(ID):
            self.isLogged = True;
            self.clientID = ID;
        send_msg = json.dumps({'mode':'login','id': ID, 'logined' : self.isLogged})
        self.OutputQueue.append(send_msg);
    def FlushOutput(self):
        for output in self.OutputQueue:
            self.clientSocket.sendall(output.encode());
            self.OutputQueue.remove(output);
            
    def login(self, loginID) -> None:
        self.isLogged = True;
        self.clientID = loginID;
    def isValidClient(self, clientID)->bool:
        return self.isLogged and self.clientID == clientID;
def getMasterSocket():
    portNumber = 1111;
    serverSocket = socket.socket(socket.AF_INET, socket.SOCKET_STREAM)
    serverSocket.bind(socket.gethostname(), portNumber)
    serverSocket.listen(5);
    serverSocket.setblocking(False);
    return serverSocket

    
def main():
    sel = selectors.DefaultSelector()
    db = Database();
    def accept(sock):
        conn, addr = sock.accept()
        conn.setbocking(False);
        clientConnection = ClientConnection(conn, db);
        sel.register(conn, selectors.EVENT_READ, clientConnection.acceptPacket)
        sel.register(conn, selectors.EVENT_WRITE, clientConnection.FlushOutput)
    masterSocket = getMasterSocket();
    sel.register(masterSocket, selectors.EVENT_READ, accept)
    while True:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj);
    

if __name__ == "__main__":
    main();