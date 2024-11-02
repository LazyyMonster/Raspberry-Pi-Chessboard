#/usr/bin/env python

from board import ChessBoard
from time import sleep
import berserk
from threading import Thread


class ChessClient:
    api_key = 'YOUR_LICHESS_TOKEN'
    humanColor = "-_-"
    gameID = "-_-"
    lastMove = "-_-"
    lastHumanMove = "-_-"
    playing = False
    winner = "-_-"

    chess = ChessBoard()
    chess.init_i2c_devices()
    ready = chess.initBoard()
    chess.setPromotion(chess.QUEEN)

    session = berserk.TokenSession(api_key)
    board = berserk.clients.Board(session)


    def sendChallenge(self):
        time, increment, rated, variant = 10, 0, False, "standard"

        print("Searching for opponent...")
        self.board.seek(time,increment,rated,variant)

        for event in self.board.stream_incoming_events():
            if event['type'] == 'gameStart':
                print("An opponent was found!")
                self.playing = True
                self.humanColor = event['game']['color']
                self.gameID = event['game']['gameId']
                if event['game']['color'] == "black":
                    self.humanColor = 1
                    print("You're playing as black!")
                else:
                    self.humanColor = 0
                    print("You're playing as white!")
                threadmain = Thread(target=self.mainLoop)
                threadmain.start()
            elif event['type'] == 'gameFinish':
                print("gameFinish")
                self.playing = False
                try:
                    self.winner = event['game']['winner']    
                #exception occurs when the game ended a draw           
                except:         
                    self.chess._game_result = self.chess.DRAW


    def getStates(self):
        for event in self.stream:
            if event['type'] == "gameFull":
                print("gameFull")
            elif event['type'] == "gameState":
                if event["status"] == "draw":
                    self.chess._game_result = self.chess.DRAW
                elif event["status"] == "resign":
                    self.winner = event["winner"]
                    print("Someone resigned.")
                    print(str(self.winner) + " is victorious!")
                    self.playing = False
                else:
                    try:
                        print(event["moves"].split()[-1])
                        self.lastMove = event["moves"].split()[-1]
                    except:
                        print("Game did not start")
            elif event['type'] == "chatLine":
                print("chatLine: " + str(event['text']))
            elif event['type'] == "opponentGoneTrue":
                if event['claimWinInSeconds'] == 0:
                    print("opponent gone!")


    def mainLoop(self):
        self.stream = self.board.stream_game_state(self.gameID)

        thread = Thread(target=self.getStates)
        thread.start()

        gameResults = ["","WHITE WINS!","BLACK WINS!","STALEMATE","DRAW BY THE FIFTHY MOVES RULE","DRAW BY THE THREE REPETITION RULE", "DRAW BY THE AGREEMENT", "DRAW"]

        while self.playing:              
            while self.chess.getTurn() == self.humanColor:
                move = self.chess.searchForMove()
                if move:
                    added = self.chess.addMove(self.chess.fromPos, self.chess.toPos)
                    if added:
                        moveInAN = self.chess.getLastTextMove(self.chess.AN)
                        self.lastHumanMove = moveInAN
                        sent = False
                        while not sent:
                            try:
                                self.board.make_move(self.gameID, moveInAN)
                                sent = True
                            except:
                                if not self.playing:
                                    sent = True
                                    print("The game has ended, the move was not sent")
                                    if self.humanColor == "white":
                                        self.chess._game_result = self.chess.BLACK_WIN
                                    else:
                                        self.chess._game_result = self.chess.WHITE_WIN
                                else:
                                    print("Error occured, the move was not sent")
               
            while not self.chess.getTurn() == self.humanColor:
                while self.lastMove == self.lastHumanMove or self.lastMove == "-_-":
                    sleep(0.01)

                fromx, fromy, tox, toy = self.chess.convertFromANtoCoordinates(self.lastMove)
                self.chess.ledON(fromx, 7-fromy, tox, 7-toy)

                move = self.chess.opponentMoveMade()
                if move:
                    added = self.chess.addMove(self.chess.fromPos, self.chess.toPos)
                    if added:
                        self.chess.ledOFF(fromx, 7-fromy, tox, -toy)
                        self.lastMove = "-_-"
        if self.winner == "black":
            self.chess._game_result = self.chess.BLACK_WIN
        else:
            self.chess._game_result = self.chess.WHITE_WIN
                        

        print("Game Over! (Reason:%s)" % gameResults[self.chess.getGameResult()])

        print(self.chess.getAllTextMoves(self.chess.AN))


def main():
    g = ChessClient()
    g.sendChallenge()

if __name__ == '__main__': main()