#/usr/bin/env python


class ChessOffline:

    def __init__(self, chessMachine, hardware):
        self.chessMachine = chessMachine
        self.hardware = hardware


    blackKing = (0, 5)
    whiteKing = (7, 5)

    gameResults = ["","WHITE WINS!","BLACK WINS!","STALEMATE","DRAW BY THE FIFTHY MOVES RULE","DRAW BY THE THREE REPETITION RULE", "DRAW BY THE AGREEMENT"]

    #kings in the centre indicate game result
    def checkKingsPositions(self, moveFrom, moveTo):
        blackKing = self.chessMachine._black_king_location
        whiteKing = self.chessMachine._white_king_location
        fromM = (moveFrom[0], 8 - moveFrom[1])
        toM = (moveTo[0], 8 - moveTo[1])

        if whiteKing == fromM:
            self.whiteKing = toM

        if blackKing == fromM:
            self.blackKing = toM

        if self.blackKing == (3, 3) and self.whiteKing == (4, 4):
            return self.chessMachine.WHITE_WIN
        elif self.blackKing == (4, 3) and self.whiteKing == (3, 4):
            return self.chessMachine.BLACK_WIN
        elif self.blackKing == (4, 3) and self.whiteKing == (4, 4):
            return self.chessMachine.DRAW_BY_AGREEMENT
        elif self.blackKing == (3, 3) and self.whiteKing == (3, 4):
            return self.chessMachine.DRAW_BY_AGREEMENT
        return 0


    def highlightLastMove(self):
        lastMove = self.chessMachine.getLastMove()
        if lastMove:
            moveFrom, moveTo = lastMove
            self.hardware.highlightMove((moveFrom[0], 8 - moveFrom[1]), (moveTo[0], 8 - moveTo[1]))
        else:
            self.hardware.resetLed()


    def mainLoop(self):
       while True:
           self.hardware.checkStartingPosition()

           while not self.chessMachine.isGameOver():
               move = self.hardware.searchForMove()

               if move:
                   moveFrom, moveTo = move
                   if moveTo:
                       added = self.chessMachine.addMove((moveFrom[0], 8 - moveFrom[1]), (moveTo[0], 8 - moveTo[1]))
                       if added:
                           #self.chessMachine.printBoard()
                           print (self.chessMachine.getLastTextMove(self.chessMachine.SAN))
                       else:
                           result = self.checkKingsPositions(moveFrom, moveTo)
                           if result:
                               self.chessMachine.endGame(result)
                               break
                       self.highlightLastMove()

                   else:
                       validMoves = self.chessMachine.getValidMoves((moveFrom[0], 8 - moveFrom[1]))
                       self.hardware.highlightValidMoves(validMoves)


           print("Game Over! (Reason:%s)" % self.gameResults[self.chessMachine.getGameResult()])
           print(self.chessMachine.getAllTextMoves(self.chessMachine.SAN))
           #print(self.chessNachine.getAllTextMoves(self.chessMachine.AN))
           #print(self.chessMachine.getAllTextMoves(self.chessMachine.LAN))
           self.chessMachine.resetBoard()
           self.hardware.resetLed()
           self.blackKing = (0, 5)
           self.whiteKing = (7, 5)
