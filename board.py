from piece import Piece
from cs1lib import *

start = None
goal = None
pressedQ = False
pressedSpaceBar = False
pressedH = True

class Board:
    def __init__(self, boardImage, width, height):
        self.img = load_image(boardImage)
        self.xlength, self.yheight = width, height

        # There are 8 squares on a checkerboard
        self.squareXLength = self.xlength/8
        self.squareYHeight = self.yheight/8
        self.positions = {}
        self.possibleMoves = {}
        self.eatingPathways = {}
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

        for move in moves:
            newX = piece.x + move[0]
            newY = piece.y + move[1]

            # If the new position is a possible move on the board
            if newX < 8 and newX >= 0 and newY < 8 and newY >= 0:

                # If the new position is not already occupied
                if (newX, newY) not in self.positions or not self.positions[(newX, newY)][1]:
                    p = Piece(newX, newY, 10, 'aqua')
                    self.possibleMoves[(newX, newY)] = p
                    # p.draw(self.xlength, self.yheight)
                
        self.checkValidEatingMoves(self.positions, piece, 0)
                

    def checkValidEatingMoves(self, positions, piece, score):
        leftDown = (-1, -1)
        rightDown = (1, -1)
        leftUp = (-1, 1)
        rightUp = (1, 1)
        moves = [leftDown, leftUp, rightDown, rightUp]

       # Check all possible directions, because 
        for move in moves:
            
            newX = piece.x + move[0]
            newY = piece.y + move[1]

            # If the current piece is next to another piece of a different color
            if (newX, newY) in positions and positions[(newX, newY)][0].color != piece.color and positions[(newX, newY)][1]:

                # If the piece were to eat the piece at (newX, newY) it would land at (destinationX, destinationY)
                destinationX = move[0] * 2 + piece.x
                destinationY = move[1] * 2 + piece.y

                # Check that this destination is not occupied
                if (destinationX, destinationY) not in positions or not positions[(destinationX, destinationY)][1]:

                    # Check that this destination is a valid position on the board
                    if destinationX < 8 and destinationX >= 0 and destinationY < 8 and destinationY >= 0:
                        p = Piece(destinationX, destinationY, 10, 'lightgreen')
                        self.possibleMoves[(destinationX, destinationY)] = p
                        # p.draw(self.xlength, self.yheight)
                        p.drawText(score, self.xlength, self.yheight)
                        # Keep track of the pathway we took to eat this piece
                        self.eatingPathways[(destinationX, destinationY)] = (piece.x, piece.y)
                        # Check that we can continue eating more pieces
                        possibleNextPositions = positions.copy()
                        eaten = possibleNextPositions[(newX, newY)][0]
                        possibleNextPositions[(newX, newY)] = (eaten, False)
                        self.checkValidEatingMoves(possibleNextPositions, p, score + 1)
            

        
    def fillBoard(self):
        for pos in self.positions.values():
            if pos[1]:
                p = pos[0]
                p.draw(self.xlength, self.yheight)
        if pressedH:
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
            backTrack = (x, y)
            currX = x
            currY = y

            # If you have eaten another piece then this new positon should be in the self.eatingPathways dictionary
            while backTrack in self.eatingPathways:
                (prevX, prevY) = self.eatingPathways[backTrack]
                eatenX = (backTrack[0] + prevX)//2
                eatenY = (backTrack[1] + prevY)//2
                eaten = self.positions[(eatenX, eatenY)][0]
                self.positions[(eatenX, eatenY)] = (eaten, False)
                self.scores[self.turn] -= 1
                backTrack = self.eatingPathways[backTrack]
        
        self.eatingPathways = {}
        return None

    def mousePress(self, mx, my):
        self.findNearbyChecker(mx, my)

    def keyUp(self, key):
        global pressedQ, pressedSpaceBar, pressedH
        if key == "q":
            pressedQ = False
        elif key == " ":
            pressedSpaceBar = False
    

    def keyDown(self, key):
        global pressedQ, pressedSpaceBar, pressedH
        if key == "q":
            pressedQ = True
            cs1_quit()
        elif key == " ":
            pressedSpaceBar = True
            # It is now the next player's turn
            self.turn += 1
            self.turn %= 2
            self.possibleMoves = {}
        elif key == "h":
            pressedH = not pressedH