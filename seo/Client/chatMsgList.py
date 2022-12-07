import json
import os
import datetime
idList =[]
msgList = {}
lastDate = datetime.datetime.now();
def getIdFileName(id):
    return id +".idlist"
def getMsgFileName(id):
    return id + ".msglist"
def getextraInfoFileName(id):
    return id + ".extra";
def readFile(id):
    if os.path.exists(getIdFileName(id)):
        f = open(getIdFileName(id), "r")
        content = f.read();
        global idList;
        idList = json.loads(content);
        f.close();
    if os.path.exists(getIdFileName(id)):
        f = open(getMsgFileName(id), "r")
        content = f.read();
        global msgList;
        msgList = json.loads(content);
        f.close();
    if os.path.exists(getextraInfoFileName(id)):
        f = open(getextraInfoFileName(id), 'r')
        content = f.read();
        extraList = json.loads(content);
        global lastDate;
        lastDate = datetime.datetime.strptime(extraList["lastDate"],'%Y-%m-%d %H:%M:%S')
        f.close();
def storeFile(id):
    f = open(getIdFileName(id), "w")
    f.write(json.dumps(idList));
    f.close()
    f = open(getMsgFileName(id), "w")
    f.write(json.dumps(msgList));
    f.close();
    extra_dict = {"lastDate" : lastDate.strftime('%Y-%m-%d %H:%M:%S')}
    f = open(getextraInfoFileName(id), "w");
    f.write(json.dumps(extra_dict));
    f.close()
def assureIdExist(id):
    try:
        idList.index(id);
    except:
        idList.append(id);
        msgList[id] = []
def updateLastDate(date: str):
    newDate = datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S');
    if newDate > lastDate:
        lastDate = newDate;