from board import Board
from cs1lib import *

WINDOW_WIDTH = 722
WINDOW_HEIGHT = 722
b = Board('checkersBoard.gif', WINDOW_WIDTH, WINDOW_HEIGHT)

def playCheckers(): 
  b.play()

def mousePress(mx, my):
  b.mousePress(mx, my)

# def mouseRelease(mx, my):
#   b.mouseRelease(mx, my)


start_graphics(playCheckers, title = "Checkers", width = WINDOW_WIDTH, height = WINDOW_HEIGHT, mouse_press= mousePress, framerate=150)