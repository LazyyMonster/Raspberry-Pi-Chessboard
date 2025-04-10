#/usr/bin/env python

from chessBoard import ChessBoard
from hardware import Hardware
from chessOffline import ChessOffline
from chessLichess import ChessLichess


def main():
    #chess logic
    chessMachine = ChessBoard()
    chessMachine.setPromotion(chessMachine.QUEEN)

    #hardware handler initialization
    hardware = Hardware()

    offline = False

    if offline:
        g = ChessOffline()
        g.mainLoop(chessMachine, hardware)
    else:
        g = ChessLichess(chessMachine, hardware)
        g.sendChallenge()

    hardware.resetLed()


#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()


