import socket
import datetime
import sys
import queue
import select
import protocol

# FROM BELL
# i WILL SEND DATA TO THE SERVER IN DICT FORMAT in JSON.dumps

class serverDatabase():
    def AddAccount(self, senderID):
        pass
    def AddMSG(self, senderID):
        pass
    def GetQuery(self, senderID, last_date):
        pass
    
class serverWork():
    def __init__(self,Mode, senderID) -> None:
        self.mode = Mode;
        self.senderID = senderID
        pass
    def __init__(self,Mode, senderID, date) -> None:
        self.__init__(Mode, senderID);
        self.date = date;
    def __init__(self,Mode, senderID, date,receiverID, msg) -> None:
        self.__init__(Mode, senderID, date)
        self.receiverID = receiverID
        self.msg = msg;
    def Do(self):
        if(Mode == protocol.clientMode.register):
            
class clientSocket():
    def __init__(self, clientSocket:socket) -> None:
        self.clientSocket = clientSocket;
        self.isLogged = False;
        self.clientID = None;
        self.sendingQueue = [];
    def returnInput(self):
        data = self.clientSocket.recv(1024);
        return self.clientID, str(data);
    def GiveInput(self,msg):
        data = self.clientSocket.sendall(msg.decode());
        
            
    def login(self, loginID) -> None:
        self.isLogged = True;
        self.clientID = loginID;
    
def main():
    portNumber = 1111;
    serverSocket = socket.socket(socket.AF_INET, socket.SOCKET_STREAM)
    serverSocket.bind(socket.gethostname(), portNumber)
    serverSocket.listen(5);
    
    clientSockets = {}
    inputs = [serverSocket]
    outputs = []
    message_queues = {}
    
    while inputs:
        readable, writable, exceptional = select.select(
            inputs, outputs, inputs)
        for s in readable:
            if s is serverSocket:
                connection, client_address = s.accept()
                connection.setblocking(0)
                inputs.append(connection)
                clientSocket[clientsocket] = connection;
                message_queues[connection] = queue.Queue()
            else:
                data = s.recv(1024)
                if data:
                    data = input(' -> ')
                    message_queues[s].put(data.encode())
                    if s not in outputs:
                        outputs.append(s)
                else:
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
                    del message_queues[s]
    
        for s in writable:
            try:
                next_msg = message_queues[s].get_nowait()
                print(next_msg)
            except queue.Empty:
                outputs.remove(s)
            else:
                s.send(next_msg)

        for s in exceptional:
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del message_queues[s]


if __name__ == "__main__":
    main();