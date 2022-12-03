import curses
import UTF_FILE
from ConnectionManagement import rcvDictList;
from ConnectionManagement import sendDictList;
import chatMsgList
from windowTools import inputBox
import datetime

class communicateWindow():
    def __init__(self, idInfo) -> None:
        self.friendWindow = friendWindow(20,20,0,0);
        self.id = idInfo
    def setErrorWindow(self):
        self.errorWindow = curses.newwin(5,120,21,0);
    def task(self):
        while self.isLogin:
            self.friendWindow.update();
            self.checkNetwork();
        return None
    def checkNetwork(self):
        if(rcvDictList.count != 0):
            rcv_dict:dict = rcvDictList[0];
            rcvDictList.remove(rcv_dict);
            self.receiveMsg(rcv_dict);
        else :
            return
    def receiveMsg(self,recv_dict):
        mode = recv_dict["mode"]
        if mode == "send":
            self.manageSend(recv_dict);
        elif mode == "request":
            self.manageReceive(recv_dict);
        else:
            pass
    def manageSend(self, dict):
        if(dict["send"] == True and dict["sender_id"] == self.id):
            chatMsgList.msgList[dict["reciever_id"]].append(dict);
        else:
            pass
    def manageReceive(self, dict):
        if(dict["requested"]== True and dict["reciever_id"] == self.id):
            chatMsgList.assureIdExist(dict["sender_id"]);
            chatMsgList.msgList[dict["sender_id"]].append(dict);
    def sendMsg(self,send_dict):
        sendDictList.append(send_dict);
class friendWindow():
    def __init__(self,n_row, n_col, start_x, start_y) -> None:
        self.window = curses.newwin(n_row, n_col, start_x, start_y);
        self.cursor = "+New id";
        self.conversationWindow = friendAddBox()
    def update(self):
        self.buttonList = chatMsgList.idList.copy()
        self.buttonList.append("+New id");
        self.checkInput();
        self.updateDraw();
        self.conversationWindow.update();
    def checkInput(self):
        inputChar = self.window.getch();
        self.handleInput(inputChar);
    def updateDraw(self):
        self.window.erase();
        self.window.border();
        countRow = 1;
        for id in self.buttonListbuttonList:
            self.drawId(id);
            countRow += 1;
        self.window.refresh();
    def handleInput(self,inputchar):
        if inputchar == curses.KEY_UP:
            next_cursor = self.getRelativeCursor(-1);
            self.changeCursor(next_cursor)
        elif inputchar == curses.KEY_DOWN:
            next_cursor = self.getRelativeCursor(1);
            self.changeCursor(next_cursor)
        else :
            self.conversationWindow.handleInput(inputchar);
    def drawId(self,rowNum, id):
        if(self.cursor == id):
            self.window.addstr(rowNum, 1, id, curses.A_REVERSE);
        else:
            self.window.addstr(rowNum, 1, id);
    def changeCursor(self, nextCursor):
        if(nextCursor == "+New id"):
            dictionary = {"new_id": ""}
            self.conversationWindow = friendAddBox(dictionary, "new_id", 20,100, 0, 21);
        else:
            self.conversationWindow = conversationWindow(self.cursor, 20,100, 0, 21)
    def getRelativeCursor(self,offset):
        currentIndex = self.buttonList.index(self.cursor);
        nextIndex = currentIndex + offset;
        if(nextIndex >= self.buttonList.count):
            nextIndex -= self.buttonList.count;
        elif(nextIndex < 0):
            nextIndex += self.buttonList.count;
        else:
            nextIndex = nextIndex
        return self.buttonList[nextIndex];
    def manageInput(self,input):
        pass
class conversationWindow():
    def __init__(self,clientId, targetId,n_row, n_col, start_y, start_x) -> None:
        self.clientId = clientId;
        self.targetId = targetId;
        self.window = curses.newwin(n_row-3,n_col,start_y,start_x);
        self.inputBox = msgAddBox(3,n_col,start_x, start_y + n_row -3);
    def handleInput(self, inputChar):
        self.inputBox.handleInput(inputChar);
    def update(self):
        self.updateDraw()
        self.inputBox.update();
    def updateDraw(self):
        msgList:list = chatMsgList.msgList[self.targetId];
        sortedList = sorted(msgList, key= lambda item:item["date"]);
        countRow = 1;
        for msg in sortedList:
            consumeLine = self.window.addstr(countRow, msg)
            countRow += consumeLine;
    def drawMsg(self,rowNum, msg)->int:
        self.window.addstr(rowNum,1,"From :" + msg["sender_id"] + ". To : " + msg["receiver_id"])
        self.window.addstr(rowNum,1,msg["message"]);
        return 3;
class msgAddBox(inputBox):
    def __init__(self,clientId, targetID, n_row, n_col, start_y, start_x) -> None:
        dict = {"msg": ""}
        cursor = "msg"
        self.clientId = clientId;
        self.targetId = targetID;
        super().__init__(dict, cursor, n_row, n_col, start_y, start_x)
    def handleInput(self, inputChar) -> None:
        if inputChar == UTF_FILE.KEY_ENTER:
            send_dict = {}
            send_dict['mode'] = 'send'
            send_dict['sender_id'] = self.clientId;
            send_dict['receiver_id'] = self.targetId;
            send_dict['message'] = self.getResult()["msg"];
            send_dict['date'] = datetime.datetime.now();
            sendDictList.append(send_dict);
            self.clearContent();
        else:
            super().handleInput(inputChar)
class friendAddBox(inputBox):
    def __init__(self, n_row, n_col, start_y, start_x) -> None:
        dict = {"new_id": ""};
        cursor = "new_id"
        super().__init__(dict, cursor, n_row, n_col, start_y, start_x)
    def handleInput(self, inputChar) -> None:
        super().handleInput(inputChar);
        if(inputChar == UTF_FILE.KEY_ENTER):
            chatMsgList.assureIdExist(self.getResult["new_id"]);