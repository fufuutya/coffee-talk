import curses
from curses import wrapper
import LoginWindow
import ConnectionManagement
def main(stdscr : 'curses._CursesWindow'):
    ConnectionManagement.runTrackThread();
    curses.noecho();
    curses.curs_set(False);
    stdscr.nodelay(True);
    currentState = LoginWindow.LoginPhase();
    while True:
        currentState = currentState.task();
        if not currentState:
            exit();
        stdscr.clear();
        
    
wrapper(main)