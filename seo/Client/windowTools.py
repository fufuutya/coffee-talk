import curses
import UTF_FILE
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

def Log(str):
    file = open("log.txt",'a')
    file.write(str);
class inputBox():
    def initialize(self, dictionary,cursor,win) -> None:
        self.cursor = cursor
        self.content = dictionary
        self.window = win
        self.window.nodelay(True);
        self.updateWindow();
    def __init__(self,dict,cursor, n_row, n_col, start_y, start_x) -> None:
        window = curses.newwin(n_row, n_col, start_y,start_x);
        self.initialize(dict, cursor, window);
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