import json
import os
import datetime
import encrypting

idList ={}
msgList = {}
lastDate = datetime.datetime.now()
private_key = None
public_key = None

def getIdFileName(id):
    return id +".idlist"
def getMsgFileName(id):
    return id + ".msglist"
def getextraInfoFileName(id):
    return id + ".extra"
def readFile(id):
    if os.path.exists(getIdFileName(id)):
        f = open(getIdFileName(id), "r")
        content = f.read()
        global idList
        idList = json.loads(content)
        for id in idList:
            key = encrypting.string2PublicKey(idList[id])
            idList[id] = key
        f.close()
    if os.path.exists(getIdFileName(id)):
        f = open(getMsgFileName(id), "r")
        content = f.read()
        global msgList
        msgList = json.loads(content)
        f.close()
    if os.path.exists(getextraInfoFileName(id)):
        f = open(getextraInfoFileName(id), 'r')
        content = f.read()
        extraList = json.loads(content)
        global lastDate
        lastDate = datetime.datetime.strptime(extraList["lastDate"],'%Y-%m-%d %H:%M:%S')
        global private_key
        global public_key
        private_key = encrypting.string2pirvatKey(extraList["private_key"])
        public_key = encrypting.string2PublicKey(extraList["public_key"])
        f.close()
def storeFile(id):
    idFileList = idList.copy()
    for id in idList.keys():
        key = idList[id]
        idFileList[id] = encrypting.key2string(key)
    f = open(getIdFileName(id), "w")
    f.write(json.dumps(idFileList))
    f.close()
    f = open(getMsgFileName(id), "w")
    f.write(json.dumps(msgList))
    f.close()
    extra_dict = {"lastDate" : lastDate.strftime('%Y-%m-%d %H:%M:%S')}
    extra_dict["private_key"] = encrypting.key2string(private_key)
    extra_dict["public_key"] = encrypting.key2string(public_key)
    f = open(getextraInfoFileName(id), "w")
    f.write(json.dumps(extra_dict))
    f.close()
def assureIdExist(id,public_key):
    if id in idList.keys():
        pass
    else:
        idList[id] = public_key
        msgList[id] = []
def isIDExist(id):
    if id in idList.keys():
        return True
    else:
        return False
def updateLastDate(date: str):
    newDate = datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
    if newDate > lastDate:
        lastDate = newDate