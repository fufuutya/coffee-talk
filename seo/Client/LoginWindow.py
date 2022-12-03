import curses
import UTF_FILE
from ConnectionManagement import rcvDictList;
from ConnectionManagement import sendDictList;
import ConnectionManagement
from CommunicateWindow import communicateWindow;
def GetNextKey(dictionary:dict, currentKey):
    currentKeyIndex = list(dictionary.keys()).index(currentKey);
    nextKeyIndex = currentKeyIndex + 1;
    if (nextKeyIndex >= len(dictionary.keys())):
        nextKeyIndex = 0;
    return list(dictionary.keys())[nextKeyIndex];
def GetInput(window):
    try:
        inputChar = window.getkey();
        test = inputChar;
    except: #when there is no input
        inputChar = -1;
    return inputChar;
class LoginPhase():
    def __init__(self) -> None:
        self.setWelcomeWindow();
        self.loginWindow = LoginWindow(5,100,6,0);
        self.isLogin  = False
    def setWelcomeWindow(self):
        self.welcomWindow = curses.newwin(5,100,0,0)
        self.welcomWindow.border();
        self.welcomWindow.addstr(1,20,"Welcom to coffee-Talk")
        self.welcomWindow.addstr(2,20,"Please Enter your password and ID")
        self.welcomWindow.refresh();
    def setErrorWindow(self):
        self.errorWindow = curses.newwin(3,100,12,0);
    def task(self):
        while not self.isLogin:
            self.loginWindow.update();
            self.checkNetwork();
        return communicateWindow();#TODO
    def checkNetwork(self):
        if(rcvDictList.count != 0):
            rcv_dict:dict = rcvDictList[0];
        else :
            return
        if "logined" in rcv_dict:
            self.loginVerify(rcv_dict);
        else :
            return
    def loginVerify(self, recv_dict):
        if(recv_dict['logined']):
            self.loginSuccess(recv_dict);
        else:
            self.loginFailed(recv_dict);
    def loginSuccess(self,recv_dict):
        self.isLogin = True;
        self.loginID = recv_dict["id"];
    def loginFailed(self,recv_dict):
        self.errorWindow.border();
        self.errorWindow.addstr(1,1,"Can't login to id" + str(recv_dict["id"]))
        self.errorWindow.refresh();
class LoginWindow():
    def __init__(self,n_row, n_col, start_y, start_x) -> None:
        self.content = {"mode":"login", "name" : "", "password" : ""}
        self.window = curses.newwin(n_row,n_col,start_y,start_x)
        self.inputBox = inputBox(self.content, "name", self.window)
        self.debug = debugWindow();
    def update(self)-> None:
        inputChar = GetInput(self.window)
        if(inputChar == UTF_FILE.KEY_ENTER):
            self.tryLogin();
        else:
            self.inputBox.handleInput(inputChar);
        self.debug.print(inputChar);
        self.inputBox.update();
    def tryLogin(self):
        sendDictList.append(self.inputBox.getResult());
class cursorWindow():
    pass

class inputBox():
    def __init__(self, dictionary,cursor,win) -> None:
        self.cursor = cursor
        self.content = dictionary
        self.window = win
        self.window.nodelay(True);
        self.updateWindow();
        curses.color_content(1,curses.COLOR_BLACK, curses.COLOR_WHITE);
        curses.color_content(2,curses.COLOR_WHITE, curses.COLOR_BLACK);
    def handleInput(self,inputChar)-> None:
        if(inputChar == -1):
            pass
        elif(inputChar == UTF_FILE.KEY_BACKSPACE):
            self.content[self.cursor] = self.content[self.cursor][:-1]
        elif(inputChar == UTF_FILE.KEY_TAB):
            self.cursor = GetNextKey(self.content,self.cursor)
        else:
            self.content[self.cursor] += inputChar;
    def update(self):
        self.window.erase();
        self.updateWindow();
    def updateWindow(self):
        self.window.border();
        selectedColor = curses.color_pair(1)
        unselectedColor = curses.color_pair(2)
        countLine = 1
        for key in self.content:
            if(key == self.cursor):
                targetColor = selectedColor;
            else:
                targetColor = unselectedColor;
            self.window.addstr(countLine,1,key + ':' + self.content[key],targetColor)
            countLine += 1;
        self.window.refresh();
    def getResult(self):
        return self.content;
    def clearContent(self):
        for key in self.content:
            self.content[key] = '';
class debugWindow():
    def __init__(self) -> None:
        self.window = curses.newwin(10,10,0,100);
    def print(self,something: int):
        self.window.erase();
        if (something != -1):
            self.window.addstr(str(something))
        self.window.refresh();