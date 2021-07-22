from board import Board
from cs1lib import *

GAME_WIDTH = 722
GAME_HEIGHT = 722
WINDOW_WIDTH = 900

b = Board('checkersBoard.gif', GAME_WIDTH, GAME_HEIGHT)

def playCheckers(): 
  b.play()

def mousePress(mx, my):
  b.mousePress(mx, my)

def keyDown(key):
  b.keyDown(key)

def keyUp(key):
  b.keyUp(key)

start_graphics(playCheckers, title = "Checkers", width = WINDOW_WIDTH, height = GAME_HEIGHT, 
      mouse_press= mousePress, framerate=150, key_press = keyDown, key_release = keyUp)