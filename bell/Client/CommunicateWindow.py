import curses
import UTF_FILE
from ConnectionManagement import rcvDictList
from ConnectionManagement import sendDictList
import chatMsgList
from windowTools import inputBox
from windowTools import GetInput
import datetime

class communicateWindow():
    def __init__(self, idInfo):
        self.id = idInfo
        self.isLogin = True
        self.friendWindow = friendWindow(self.id, 10,20,0,0)
        self.setErrorWindow()
        
    def setErrorWindow(self):
        self.errorWindow = curses.newwin(5,120,11,0)
        
    def showErrMessage(self, str):
        self.errorWindow.border()
        self.errorWindow.addstr(1,1,str)
        
    def task(self): #DO TASK
        while self.isLogin:
            self.friendWindow.update() #update friendWindow
            self.checkNetwork() #check network
        return None
    
    def checkNetwork(self):
        if(len(rcvDictList)):
            rcv_dict:dict = rcvDictList[0]
            rcvDictList.remove(rcv_dict)
            self.receiveMsg(rcv_dict)
        else :
            return
        
    def receiveMsg(self,recv_dict):
        mode = recv_dict["mode"]
        if mode == "send":
            self.manageSend(recv_dict)
        elif mode == "request":
            self.manageReceive(recv_dict)
        elif mode == "check":
            self.manageCheck(recv_dict)
        else:
            pass
        
    def manageCheck(self, dict):
        if dict['checked']:
            chatMsgList.assureIdExist(dict['check_id'])
        else:
            self.showErrMessage("There is no such ID" + dict["check_id"])
            
    def manageSend(self, dict):
        if(dict["sent"] == True and dict["sender_id"] == self.id):
            chatMsgList.msgList[dict["receiver_id"]].append(dict)
        else:
            self.showErrMessage("There is no such ID" + dict["receiver_id"])
            
    def manageReceive(self, dict):
        if(dict["requested"]== True and dict["reciever_id"] == self.id):
            chatMsgList.assureIdExist(dict["sender_id"])
            chatMsgList.msgList[dict["sender_id"]].append(dict)
            
    def sendMsg(self,send_dict):
        sendDictList.append(send_dict)
        
class friendWindow():
    def __init__(self,id, n_row, n_col, start_y, start_x) -> None:
        self.id = id
        self.window = curses.newwin(n_row, n_col, start_y, start_x)
        self.cursor = "+New id"
        self.conversationWindow = friendAddBox(3, 100, 0, n_col+start_x)
        self.n_row = n_row
        self.n_col = n_col
        self.start_y = start_y
        self.start_x = start_x
        
    def update(self):
        self.buttonList = chatMsgList.idList.copy()
        self.buttonList.append("+New id")
        self.checkInput()
        self.updateDraw()
        self.conversationWindow.update()
        
    def checkInput(self):
        inputChar = GetInput(self.window)
        self.handleInput(inputChar)
        
    def updateDraw(self):
        self.window.erase()
        self.window.border()
        countRow = 1
        for id in self.buttonList:
            self.drawId(countRow, id)
            countRow += 1
        self.window.refresh()
        
    def handleInput(self,inputchar):
        if inputchar == UTF_FILE.KEY_TAB:
            next_cursor = self.getRelativeCursor(-1)
            self.changeCursor(next_cursor)
        else :
            self.conversationWindow.handleInput(inputchar)
            
    def drawId(self,rowNum, id):
        if(self.cursor == id):
            self.window.addstr(rowNum, 1, id, curses.A_REVERSE)
        else:
            self.window.addstr(rowNum, 1, id)
            
    def changeCursor(self, nextCursor):
        self.cursor = nextCursor
        self.conversationWindow.window.erase()
        if(self.cursor == "+New id"):
            dictionary = {"new_id": ""}
            self.conversationWindow = friendAddBox(3, 100, 0, self.n_col+self.start_x)
        else:
            self.conversationWindow = conversationWindow(self.id, self.cursor, 10, 50, 0, 21)
            
    def getRelativeCursor(self,offset):
        currentIndex = self.buttonList.index(self.cursor)
        nextIndex = currentIndex + offset
        if(nextIndex >= len(self.buttonList)):
            nextIndex -= len(self.buttonList)
        elif(nextIndex < 0):
            nextIndex += len(self.buttonList)
        else:
            nextIndex = nextIndex
        return self.buttonList[nextIndex]
    
    def manageInput(self,input):
        pass
    
class conversationWindow():
    def __init__(self,clientId, targetId, n_row, n_col, start_y, start_x) -> None:
        self.clientId = clientId
        self.targetId = targetId
        self.window = curses.newwin(n_row-3, n_col, start_y, start_x)
        self.inputBox = msgAddBox(self.clientId, self.targetId, 3, n_col, start_y + n_row-3, start_x)
        
    def handleInput(self, inputChar):
        self.inputBox.handleInput(inputChar)
        
    def update(self):
        self.updateDraw()
        self.inputBox.update()
        
    def updateDraw(self):
        msgList:list = chatMsgList.msgList[self.targetId]
        sortedList = sorted(msgList, key= lambda item:item["date"])
        countRow = 1
        for msg in sortedList:
            consumeLine = self.drawMsg(countRow, msg)
            countRow += consumeLine
        alllines = int(len(sortedList) * 3.5)
        
        self.window.refresh()
        
    def drawMsg(self,rowNum, msg)->int:
        self.window.addstr(rowNum, 1, "From :" + msg["sender_id"] + ". To : " + msg["receiver_id"])
        self.window.addstr(rowNum+1, 1, msg["message"])
        return 3
    
class msgAddBox(inputBox):
    def __init__(self,clientId, targetID, n_row, n_col, start_y, start_x) -> None:
        dict = {"msg": ""}
        cursor = "msg"
        self.clientId = clientId
        self.targetId = targetID
        super().__init__(dict, cursor, n_row, n_col, start_y, start_x)
        
    def handleInput(self, inputChar) -> None:
        if inputChar == UTF_FILE.KEY_ENTER:
            send_dict = {}
            send_dict['mode'] = 'send'
            send_dict['sender_id'] = self.clientId
            send_dict['receiver_id'] = self.targetId
            send_dict['message'] = self.getResult()["msg"]
            send_dict['date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sendDictList.append(send_dict)
            self.clearContent()
        else:
            super().handleInput(inputChar)
            
class friendAddBox(inputBox):
    def __init__(self, n_row, n_col, start_y, start_x) -> None:
        dict = {"new_id": ""}
        cursor = "new_id"
        super().__init__(dict, cursor, n_row, n_col, start_y, start_x)
        
    def handleInput(self, inputChar) -> None:
        if(inputChar == UTF_FILE.KEY_ENTER):
            sendMsg = {"mode" : "check"}
            sendMsg['check_id'] = self.getResult()['new_id']
            sendDictList.append(sendMsg)
        else:
            super().handleInput(inputChar)