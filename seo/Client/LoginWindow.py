import curses
import UTF_FILE
from ConnectionManagement import rcvDictList;
from ConnectionManagement import sendDictList;
from CommunicateWindow import communicateWindow;
from windowTools import inputBox
from windowTools import GetInput

class LoginPhase():
    def __init__(self) -> None:
        self.setWelcomeWindow();
        self.loginWindow = LoginWindow(5,100,7,0);
        self.setErrorWindow();
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
        return communicateWindow(self.loginID);#TODO
    def checkNetwork(self):
        if(len(rcvDictList) != 0):
            rcv_dict:dict = rcvDictList[0];
            rcvDictList.remove(rcv_dict);
        else :
            return
        if "logined" in rcv_dict:
            self.loginVerify(rcv_dict);
        elif "registered" in rcv_dict:
            self.registerVerify(rcv_dict);
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
        self.showErrorMsg("Can't login to id" + str(recv_dict["id"]));
    def registerVerify(self, recv_dict):
        if(recv_dict["registered"]):
            self.showErrorMsg("register complete");
        else:
            self.showErrorMsg("Already registered");
    def showErrorMsg(self,msg):
        self.errorWindow.erase();
        self.errorWindow.border();
        self.errorWindow.addstr(1,1,msg);
        self.errorWindow.refresh();
class LoginWindow():
    def __init__(self,n_row, n_col, start_y, start_x) -> None:
        self.content = {"mode":"login", "id" : "", "userName" : ""}
        self.inputBox = inputBox(self.content, "id",n_row, n_col, start_y, start_x)
        self.debug = debugWindow();
    def update(self)-> None:
        inputChar = GetInput(self.inputBox.window);
        if(inputChar == UTF_FILE.KEY_ENTER):
            self.tryLogin();
        else:
            self.inputBox.handleInput(inputChar);
        self.debug.print(inputChar);
        self.inputBox.update();
    def tryLogin(self):
        sendDictList.append(self.inputBox.getResult());


class debugWindow():
    def __init__(self) -> None:
        self.window = curses.newwin(10,10,0,100);
    def print(self,something: int):
        self.window.erase();
        if (something != -1):
            self.window.addstr(str(something))
        self.window.refresh();