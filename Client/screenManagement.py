import curses
standardScreen = []
def setScreen(stdscr):
    standardScreen.append(stdscr);
def clearScreen():
    standardScreen[0].clear();
    standardScreen[0].refresh();