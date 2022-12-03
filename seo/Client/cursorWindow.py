import curses
import UTF_FILE
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
        
        
            