import socket
import selectors
import sys
import json
from option import *
from threading import Thread
rcvDictList = [];
sendDictList = [];
client = None;
def getClient():
    if(client == None):
        client = connect()
    return client
def connect():
    reconnect = True
    while reconnect:
        server_ip = '192.168.0.103'
        server_port = 1111
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
def trackMsg():
    readSel = selectors.DefaultSelector();
    writeSel = selectors.DefaultSelector();
    readSel.register(client, selectors.EVENT_READ, readContent);
    writeSel.register(client, selectors.EVENT_WRITE, writeContent);
    while True:
        events = readSel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj);
        events = writeSel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj);
def readContent(conn:socket.socket):
    recv_msg = conn.recv(1024).decode('utf-8');
    if recv_msg:
        recv_json = json.loads(recv_msg);
        rcvDictList.append(recv_json);
    else:
        return
def writeContent(conn:socket.socket):
    if(sendDictList.count != 0):
        sendDict = sendDictList[0];
        send_msg = json.dump(sendDict);
        conn.sendall(send_msg);
        sendDictList.remove(sendDict);
def runTrackThread():
    connect();
    trackThread = Thread(target= trackMsg);
    trackThread.start();