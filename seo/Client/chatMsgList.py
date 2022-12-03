import json
idList =[]
msgList = {}
def readFile(idfilename,msgfileName):
    f = open(idfilename, "r")
    content = f.read();
    msgList = json.loads(content);
    f.close();
    f = open(msgfileName, "r")
    content = f.read();
    msgList = json.loads(content);
    f.close();
def storeFile(idfilename,msgfileName):
    f = open(idfilename, "w")
    f.write(json.dumps(idList));
    f.close()
    f = open(msgfileName, "w")
    f.write(json.dumps(idList));
    f.close();
def assureIdExist(id):
    try:
        idList.index(id);
    except:
        idList.append(id);
        msgList[id] = {}