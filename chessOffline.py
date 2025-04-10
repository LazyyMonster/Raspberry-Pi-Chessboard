#/usr/bin/env python


class ChessOffline:

    blackKing = (0, 5)
    whiteKing = (7, 5)

    gameResults = ["","WHITE WINS!","BLACK WINS!","STALEMATE","DRAW BY THE FIFTHY MOVES RULE","DRAW BY THE THREE REPETITION RULE", "DRAW BY THE AGREEMENT"]

    #kings in the centre indicate game result
    def checkKingsPositions(self, moveFrom, moveTo, chessMachine):
        blackKing = chessMachine._black_king_location
        whiteKing = chessMachine._white_king_location
        fromM = (moveFrom[0], 8 - moveFrom[1])
        toM = (moveTo[0], 8 - moveTo[1])

        if whiteKing == fromM:
            self.whiteKing = toM

        if blackKing == fromM:
            self.blackKing = toM

        if self.blackKing == (3, 3) and self.whiteKing == (4, 4):
            return chessMachine.WHITE_WIN
        elif self.blackKing == (4, 3) and self.whiteKing == (3, 4):
            return chessMachine.BLACK_WIN
        elif self.blackKing == (4, 3) and self.whiteKing == (4, 4):
            return chessMachine.DRAW_BY_AGREEMENT
        elif self.blackKing == (3, 3) and self.whiteKing == (3, 4):
            return chessMachine.DRAW_BY_AGREEMENT
        return 0


    def highlightLastMove(self, chessMachine, hardware):
        lastMove = chessMachine.getLastMove()
        if lastMove:
            moveFrom, moveTo = lastMove
            hardware.highlightMove((moveFrom[0], 8 - moveFrom[1]), (moveTo[0], 8 - moveTo[1]))


    def mainLoop(self, chessMachine, hardware):
       hardware.checkStartingPosition()

       while not chessMachine.isGameOver():
           move = hardware.searchForMove()

           if move:
               moveFrom, moveTo = move
               if moveTo:
                   added = chessMachine.addMove((moveFrom[0], 8 - moveFrom[1]), (moveTo[0], 8 - moveTo[1]))
                   if added:
                       #chessMachine.printBoard()
                       print (chessMachine.getLastTextMove(chessMachine.SAN))
                   else:
                       result = self.checkKingsPositions(moveFrom, moveTo, chessMachine)
                       if result:
                           chessMachine.endGame(result)
                           break
                   self.highlightLastMove(chessMachine, hardware)

               else:
                   validMoves = chessMachine.getValidMoves((moveFrom[0], 8 - moveFrom[1]))
                   hardware.highlightValidMoves(validMoves)


       print("Game Over! (Reason:%s)" % self.gameResults[chessMachine.getGameResult()])
       print(chessMachine.getAllTextMoves(chessMachine.SAN))
       #print(chessNachine.getAllTextMoves(chessMachine.AN))
       #print(chessMachine.getAllTextMoves(chessMachine.LAN))
