#/usr/bin/env python

from board import ChessBoard


class ChessClient:

    def mainLoop(self):      
         
        chess = ChessBoard()
        chess.init_i2c_devices()
        ready = chess.initBoard()

        #setting default promotion piece to queen
        chess.setPromotion(chess.QUEEN) 

        blackKing = (0, 5)
        whiteKing = (7, 5)

        gameResults = ["","WHITE WINS!","BLACK WINS!","STALEMATE","DRAW BY THE FIFTHY MOVES RULE","DRAW BY THE THREE REPETITION RULE", "DRAW BY THE AGREEMENT"]

        while ready:              
            if not chess.isGameOver():
                #move is True if some reed switch is closed
                move = chess.searchForMove()  
                if move:
                    #added is True if move was added successfully
                    added = chess.addMove(chess.fromPos, chess.toPos) 
                    if added:
                        #chess.printBoard()
                        print (chess.getLastTextMove(chess.SAN))
                    else:
                        toSq = chess.toPos
                        fromSq = chess.fromPos
                        if toSq == [3, 3] or toSq == [4, 3] or toSq == [3, 4] or toSq == [4, 4]:
                            if chess._black_king_location[0] == fromSq[0] and chess._black_king_location[1] == fromSq[1]:
                                blackKing = (toSq[0], toSq[1])
                            elif chess._white_king_location[0] == fromSq[0] and chess._white_king_location[1] == fromSq[1]:
                                whiteKing = (toSq[0], toSq[1])
                        if chess.getReason() == 2:
                            if chess.fromPos == chess.previoustoPos and chess.toPos != chess.previousfromPos:                  
                                chess.fromPos = chess.previousfromPos
                            else:
                                chess.undo()                    
                        if blackKing == (3, 3) and whiteKing == (4, 4):
                            chess._game_result = chess.WHITE_WIN
                        elif blackKing == (4, 3) and whiteKing == (3, 4):
                            chess._game_result = chess.BLACK_WIN
                        elif blackKing == (4, 3) and whiteKing == (4, 4):
                            chess._game_result = chess.DRAW_BY_AGREEMENT
                        elif blackKing == (3, 3) and whiteKing == (3, 4):
                            chess._game_result = chess.DRAW_BY_AGREEMENT
                        

            elif chess.isGameOver():
                ready = False
                print("Game Over! (Reason:%s)" % gameResults[chess.getGameResult()]) 
                #print(chess.getAllTextMoves(chess.AN))
                print(chess.getAllTextMoves(chess.SAN))
                #print(chess.getAllTextMoves(chess.LAN))


def main():
    g = ChessClient()
    g.mainLoop()

 
#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()


