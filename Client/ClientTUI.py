import curses
from curses import wrapper
import LoginWindow
import ConnectionManagement
import screenManagement

def main(stdscr : 'curses._CursesWindow'):
    ConnectionManagement.runTrackThread()
    curses.noecho()
    curses.curs_set(False)
    stdscr.nodelay(True)
    screenManagement.setScreen(stdscr)
    currentState = LoginWindow.LoginPhase()
    while True:
        stdscr.nodelay(True)
        currentState = currentState.task()
        if not currentState:
            exit()
        stdscr.clear()
        stdscr.refresh()

wrapper(main)