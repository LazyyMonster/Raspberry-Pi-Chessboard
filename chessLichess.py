#/usr/bin/env python

import berserk
from threading import Thread


class ChessLichess:

    def __init__(self, chessMachine, hardware):
        self.chess = chessMachine
        self.hardware = hardware


    challengeAI = True
    api_key = 'its YOUR key!'
    playerColor = None
    gameID = None
    highlighted = None

    session = berserk.TokenSession(api_key)
    client = berserk.Client(session)


    def sendChallenge(self):
        self.hardware.checkStartingPosition()
        try:
            if self.challengeAI:
                self.sendChallengeAI()
            else:
                self.sendChallengePlayer()
        except:
            print ("error in sendChallenge")


    def sendChallengePlayer(self):
        time, increment, rated, variant = 10, 0, False, "standard"

        print("Searching for opponent...")
        response = self.client.board.seek(time,increment,rated,variant)

        events = self.client.board.stream_incoming_events()
        for event in events:
            #print (f"{event=}")
            if event['type'] == 'gameStart':
                print("An opponent was found!")

                self.gameID = event['game']['fullId']
                self.playerColor = 0 if (event['game']['color'] == 'white') else 1
                self.highlighted = False if self.playerColor else True

                print ('''You're playing as black!''' if self.playerColor else '''You're playing as white!''')

                threadmain = Thread(target=self.mainLoop)
                threadmain.start()


    def sendChallengeAI(self):
        level = 2
        color = "white"

        print ("Sending AI challenge...")
        response = self.client.challenges.create_ai(level, color= color)

        self.playerColor = 0 if (color == 'white') else 1
        self.highlighted = False if self.playerColor else True

        if response['status']['name'] == 'started':
            self.gameID = response['fullId']

            print ("AI challenge started!")
            print ('''You're playing as black!''' if self.playerColor else '''You're playing as white!''')

            threadmain = Thread(target=self.mainLoop)
            threadmain.start()


    def getStates(self):
        for event in self.stream:
#            print (f"{event=}")
            if event['type'] == "gameFull":
                print("gameFull")
            elif event['type'] == "gameState":
                if event["status"] == "draw":
                    self.chess._game_result = self.chess.DRAW
                elif event["status"] == "resign":
                    self.winner = event["winner"]
                    if self.winner == "black":
                        self.chess.endGame(self.chess.BLACK_WIN)
                    else:
                        self.chess.endGame(self.chess.WHITE_WIN)

                    print("Someone resigned.")
                    print(str(self.winner) + " is victorious!")
                else:
                    try:
                        print(event["moves"].split()[-1])
                        moveAN = event["moves"].split()[-1]
                        self.makeOpponentMove(moveAN)
                    except:
                        print("Game did not start")

            elif event['type'] == "chatLine":
                print("chatLine: " + str(event['text']))
            elif event['type'] == "opponentGoneTrue":
                if event['claimWinInSeconds'] == 0:
                    print("opponent gone!")


    def highlightLastMove(self):
        lastMove = self.chess.getLastMove()
        if lastMove:
            moveFrom, moveTo = lastMove
            self.hardware.highlightMove((moveFrom[0], 8 - moveFrom[1]), (moveTo[0], 8 - moveTo[1]))


    def makeOpponentMove(self, moveAN):
        added = self.chess.addTextMove(moveAN)
        if added:
            self.highlightLastMove()
            self.highlighted = True
        else:
            print ("error in makeOpponentMove")


    def makePlayerMove(self):
        if self.highlighted:
            move = self.hardware.searchForMove()
            if move:
                moveFrom, moveTo = move
                if moveTo:
                    added = self.chess.addMove((moveFrom[0], 8 - moveFrom[1]), (moveTo[0], 8 - moveTo[1]))
                    if added:
                        self.highlightLastMove()
                        moveInAN = self.chess.getLastTextMove(self.chess.AN)
                        print (f"{moveInAN=}")
                        while True:
                            try:
                                response = self.client.board.make_move(self.gameID, moveInAN)
                                self.highlighted = False
                                break
                            except:
                                print ("move not sent")


    def mainLoop(self):
        self.stream = self.client.board.stream_game_state(self.gameID)
        thread = Thread(target=self.getStates)
        thread.start()

        gameResults = ["","WHITE WINS!","BLACK WINS!","STALEMATE","DRAW BY THE FIFTHY MOVES RULE","DRAW BY THE THREE REPETITION RULE", "DRAW BY THE AGREEMENT", "DRAW"]

        while not self.chess.isGameOver():
            if self.chess.getTurn() == self.playerColor:
                 self.makePlayerMove()


        print("Game Over! (Reason:%s)" % gameResults[self.chess.getGameResult()])
        print(self.chess.getAllTextMoves(self.chess.SAN))
