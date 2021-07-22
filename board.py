from piece import Piece
from cs1lib import *

start = None
goal = None
pressedQ = False
pressedSpaceBar = False

class Board:
    def __init__(self, boardImage, width, height):
        self.img = load_image(boardImage)
        self.xlength, self.yheight = width, height

        # There are 8 squares on a checkerboard
        self.squareXLength = self.xlength/8
        self.squareYHeight = self.yheight/8
        self.positions = {}
        self.possibleMoves = {}
        self.turn = 1
        self.colors = ['red', 'white']
        self.scores = [12, 12]

        startY = 0
        startX = 1

        while startY < 3:
            while startX < 8:
                p = Piece(startX, startY, 40, self.colors[0])
                self.positions[(startX, startY)] = (p, True)
                startX += 2
            startX += 1
            startX %= 2
            startY += 1

        startY = 5
        startX = 0
        while startY < 8:
            while startX < 8:
                p = Piece(startX, startY, 40, self.colors[1])
                self.positions[(startX, startY)] = (p, True)
                startX += 2
            startX += 1
            startX %= 2
            startY += 1

        
        
        
    def play(self):

        draw_image(self.img, 0, 0)
        self.instructions(str(self.scores[0]), str(self.scores[1]))
        self.fillBoard()

    def instructions(self, score0, score1):
        fontSize = 25
        set_font_size(fontSize)
        set_font_bold()

        draw_text(score0, self.xlength + 70, self.yheight -50 )
        draw_text(score1, self.xlength + 70, 50 )

        draw_text("Press", self.xlength + 50, self.yheight//2 - fontSize * 3)
        draw_text("SPACEBAR", self.xlength + 20, self.yheight//2 - fontSize)
        draw_text("to end", self.xlength + 50, self.yheight//2 + fontSize)
        draw_text("your turn", self.xlength + 35, self.yheight//2 + fontSize * 3)
        

        

    def checkValidMoves(self, piece):
        valid = []
        leftDown = (-1, -1)
        rightDown = (1, -1)
        leftUp = (-1, 1)
        rightUp = (1, 1)

        if piece.color == self.colors[0]:
            moves = [leftUp, rightUp]

        else:
            moves = [leftDown, rightDown]
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
                
                self.checkValidEatingMoves(piece, newX, newY, move)
                

    def checkValidEatingMoves(self, piece, newX, newY, move):
        leftDown = (-1, -1)
        rightDown = (1, -1)
        leftUp = (-1, 1)
        rightUp = (1, 1)
        moves = [leftDown, leftUp, rightDown, rightUp]

        # If the current piece can eat another piece
        if (newX, newY) in self.positions and self.positions[(newX, newY)][0].color != piece.color and self.positions[(newX, newY)][1]:
            destinationX = move[0] * 2 + piece.x
            destinationY = move[1] * 2 + piece.y



            # Check that the destination is not occupied
            if (destinationX, destinationY) not in self.positions or (not self.positions[(destinationX, destinationY)][1]):
                eatenPiece = self.positions[(newX, newY)][0]
                p = Piece(destinationX, destinationY, 40, 'green')
                self.possibleMoves[(destinationX, destinationY)] = p
                p.draw(self.xlength, self.yheight)

                for move in moves:
                    nX = destinationX + move[0]
                    nY = destinationY + move[1]

        
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

        # If you have just clicked on a checker piece 
        if (x, y) in self.positions and self.positions[(x, y)][1] == True:
            p = self.positions[(x, y)][0]
            # If it is this player's turn
            if self.colors[self.turn] == p.color:
                self.possibleMoves = {}
                start = p
                self.checkValidMoves(start)
                return p
        
        
        # If you are trying to make a move and it is this player's turn
        if (x, y) in self.possibleMoves and start != None and self.colors[self.turn] == start.color:
            p = Piece(x, y, 40, start.color)
            self.positions[(start.x, start.y)] = (start, False)
            self.positions[(x, y)] = (p, True)
            self.possibleMoves = {}


            # If you have eaten another piece then the difference between the start and current vertex is more than 1
            if abs(start.x - x) + abs(start.y - y) > 2:
                # We have eaten something, let us find out where it was
                eatenX = (start.x + x)//2
                eatenY = (start.y + y)//2
                eaten = self.positions[(eatenX, eatenY)][0]
                self.positions[(eatenX, eatenY)] = (eaten, False)
                print(self.scores)
                self.scores[self.turn] -= 1
                print(self.scores)


        return None

    def mousePress(self, mx, my):
        self.findNearbyChecker(mx, my)

    def keyUp(self, key):
        global pressedQ, pressedSpaceBar
        if key == "q":
            pressedQ = False
        elif key == " ":
            pressedSpaceBar = False
    

    def keyDown(self, key):
        global pressedQ, pressedSpaceBar
        if key == "q":
            pressedQ = True
            cs1_quit()
        elif key == " ":
            pressedSpaceBar = True
            # It is now the next player's turn
            self.turn += 1
            self.turn %= 2
            self.possibleMoves = {}