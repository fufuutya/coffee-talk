import curses
import UTF_FILE
def GetNextKey(dictionary:dict, currentKey):
    currentKeyIndex = list(dictionary.keys()).index(currentKey);
    nextKeyIndex = currentKeyIndex + 1;
    if (nextKeyIndex >= len(dictionary.keys())):
        nextKeyIndex = 0;
    return list(dictionary.keys())[nextKeyIndex];
class cursorWindow():
    def __init__(self) -> None:
        self.isCursorSelected = False;
        self.cursor = None;
        self.windowList = []
    def addWindow(self,window):
        self.windowList.append(window);
    def update(self):
        for window in self.windowList:
            window.update();
        
    def deleteWindow(self,window:curses.window):
        try:
            if(self.cursor == window):
                self.cursor = None;
                self.isCursorSelected = False;
            self.windowList.remove(window);
            del window;
        except:
            pass
    def handleInput(self, input)->bool:
        isSelfManageInput = False
        isCursorManageInput = False
        if (isCursorManageInput):
            isCursorManageInput = self.cursor.handleInput(input);
        if (not isCursorManageInput):
            isSelfManageInput = self.manageInput(input);
        isManageinput = isCursorManageInput or isSelfManageInput;
        return isManageinput;
    def manageInput(self,input)->bool:
        if (input == UTF_FILE.KEY_ESC):
            if (self.isCursorSelected):
                self.isCursorSelected = False;
                return True;
            else:
                return False;
        elif(input == UTF_FILE.KEY_ENTER):
            if(self.cursor != None and self.isCursorSelected == False):
                self.isCursorSelected = True;
                return True;
            else:
                return False;
        elif(input == UTF_FILE.KEY_TAB):
            self.cursor = self.getNextWindow();
            return True;
    def getNextWindow(self):
        try :
            index = self.windowList.index(self.cursor);
            index = index + 1;
            if(self.windowList.count <= index):
                return self.windowList[0];
            else:
                return self.windowList[index];
        except:
            if(self.windowList.count > 0):
                return self.windowList[0];
            else:
                return None;
class inputBox():
    def __init__(self, dictionary,cursor,win) -> None:
        self.cursor = cursor
        self.content = dictionary
        self.window = win
        self.window.nodelay(True);
        self.updateWindow();
    def __init__(self,dict,cursor, n_row, n_col, start_y, start_x) -> None:
        window = curses.newwin(n_row, n_col, start_y,start_x);
        self.__init__(dict, cursor, window)
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
        countLine = 1
        for key in self.content:
            if(key == self.cursor):
                self.window.addstr(countLine,1,key + ':' + self.content[key],curses.A_REVERSE)
            else:
                self.window.addstr(countLine,1,key + ':' + self.content[key])
            countLine += 1;
        self.window.refresh();
    def getResult(self):
        return self.content;
    def clearContent(self):
        for key in self.content:
            self.content[key] = '';