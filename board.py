# Stopping Here, Because I can't figure out how to plot on the same plot the possible moves
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Circle
from piece import Piece
from cs1lib import *

start = None
goal = None

class Board:
    def __init__(self, boardImage, width, height):
        self.img = load_image(boardImage)
        self.xlength, self.yheight = width, height

        # There are 8 squares on a checkerboard
        self.squareXLength = self.xlength/8
        self.squareYHeight = self.yheight/8
        self.positions = {}
        self.possibleMoves = {}

        startY = 0
        startX = 1
        while startY < 3:
            while startX < 8:
                p = Piece(startX, startY, 40, 'red')
                self.positions[(startX, startY)] = (p, True)
                startX += 2
            startX += 1
            startX %= 2
            startY += 1

        startY = 5
        startX = 0
        while startY < 8:
            while startX < 8:
                p = Piece(startX, startY, 40, 'white')
                self.positions[(startX, startY)] = (p, True)
                startX += 2
            startX += 1
            startX %= 2
            startY += 1

        
        
        
    def play(self):

        draw_image(self.img, 0, 0)
        self.fillBoard()
        pass
        

    def checkValidMoves(self, piece):
        valid = []
        leftDown = (-1, -1)
        rightDown = (1, -1)
        leftUp = (-1, 1)
        rightUp = (1, 1)
        moves = [leftDown, leftUp, rightDown, rightUp]
        print(piece.x, piece.y)

        for move in moves:
            newX = piece.x + move[0]
            newY = piece.y + move[1]

            # If the new position is a possible move on the board
            if newX < 8 and newX >= 0 and newY < 8 and newY >= 0:

                # If the new position is not already occupied
                if (newX, newY) not in self.positions or not self.positions[(newX, newY)][1]:
                    p = Piece(newX, newY, 40, 'green')
                    self.possibleMoves[(newX, newY)] = p
                    p.draw(self.xlength, self.yheight)

                # If the current piece can eat another piece
                if (newX, newY) in self.positions and self.positions[(newX, newY)][0].color != self.positions[(piece.x, piece.y)][0].color:
                    destinationX = move[0] * 2 + piece.x
                    destinationY = move[1] * 2 + piece.y

                    # Check that the destination is not occupied
                    if (destinationX, destinationY) not in self.positions or (not self.positions[(destinationX, destinationY)][1]):
                        eatenPiece = self.positions[(newX, newY)][0]
                        p = Piece(destinationX, destinationY, 40, 'green')
                        self.possibleMoves[(destinationX, destinationY)] = p
                        # self.positions[(newX, newY)] = (eatenPiece, False)
                        p.draw(self.xlength, self.yheight)

        

        
    def fillBoard(self):
        for pos in self.positions.values():
            if pos[1]:
                p = pos[0]
                p.draw(self.xlength, self.yheight)
            
        for pos in self.possibleMoves.values():
            p = pos
            p.draw(self.xlength, self.yheight)

    def findNearbyChecker(self, mx, my):
        global start
        x = int(mx // self.squareXLength)
        y = int(my // self.squareYHeight)


        if (x, y) in self.positions and self.positions[(x, y)][1] == True:
            self.possibleMoves = {}
            p = self.positions[(x, y)][0]
            start = p
            self.checkValidMoves(start)
            return p
        
        
        if (x, y) in self.possibleMoves and start != None:
            p = Piece(x, y, 40, start.color)
            self.positions[(start.x, start.y)] = (start, False)
            self.positions[(x, y)] = (p, True)
            self.possibleMoves = {}

        return None

    def mousePress(self, mx, my):
        self.findNearbyChecker(mx, my)

        
