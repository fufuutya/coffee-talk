import socket
import selectors
import sys
import json
import select
from option import *
from threading import Thread
from windowTools import Log
import ssl
rcvDictList = [];
sendDictList = [];
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT);
context.load_verify_locations("C:/Users/USER/CA.pem")
client = None;
def connect():
    reconnect = True
    while reconnect:
        server_ip = '127.0.0.1'
        server_port = 1111
        newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client = context.wrap_socket(newSocket, server_hostname= "coffeeTalk");
        client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            client.connect((server_ip, int(server_port)))
            print('Connected to server')
            reconnect = False
        except :
            print('Connection failed')
            reconnect = convert_yesno_to_bool(input('Do you want to reconnect? (y/n): '))
            if reconnect == False:
                print('Goodbye')
                sys.exit()
    return client
def trackMsg(client):
    readSel = selectors.DefaultSelector();
    writeSel = selectors.DefaultSelector();
    readSel.register(client, selectors.EVENT_READ, readContent);
    writeSel.register(client, selectors.EVENT_WRITE, writeContent);
    while True:
        rcli, wcli, xcli = select.select([client],[client],[client]);
        for rMat in rcli:
            readContent(rMat)
        for wMat in wcli:
            writeContent(wMat)
        for xMat in xcli:
            Log(xMat)
def readContent(conn:socket.socket):
    recv_msg = conn.recv(1024)
    recv_msg = recv_msg.decode('utf-8');
    if recv_msg:
        recv_json = json.loads(recv_msg);
        rcvDictList.append(recv_json);
    else:
        return
def writeContent(conn:socket.socket):
    if(len(sendDictList) != 0):
        sendDict = sendDictList[0];
        send_msg = json.dumps(sendDict);
        conn.sendall(send_msg.encode());
        sendDictList.remove(sendDict);
def runTrackThread():
    client = connect();
    trackThread = Thread(target= trackMsg, args= [client]);
    trackThread.start();