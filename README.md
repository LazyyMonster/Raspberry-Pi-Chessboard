# Python modules for playing chess on a real chessboard with Raspberry Pi on Lichess.org using Lichess API or offline.
![build4](https://github.com/user-attachments/assets/5b82a02f-5660-491e-b5d7-ee4260f8efc3)

# Project Assumptions
Detection of chess piece presence on a given square using reed switches. Each chess piece has neodymium magnets attached to its base. Movement recognition and recording of moves are based on the initial position of each piece. When a piece is lifted, LEDs display the possible moves for that piece in its current position.

There are two game modes available:
1. 2 players (offline)
2. Single player vs. random online opponent - the opponent's moves are highlighted with LEDs.

A Raspberry Pi connects to the the Lichess API. The progress of the game (time and current board position) can be observed from any device through the Lichess.org website. To use online mode paste your private Token for Lichess API access (assigned to your account). You can generate it in settings of your account on Lichess.org.

# Block diagram
![blockDiagram](https://github.com/user-attachments/assets/429f3d03-8993-4b48-a59b-6e75871d6c89)

# My custom chessboard
![build1](https://github.com/user-attachments/assets/218560a6-50aa-4428-bc7f-2e911624cc24)
![build2](https://github.com/user-attachments/assets/d09ba70e-2126-40a5-9f75-b9362a11e1d9)
![build3](https://github.com/user-attachments/assets/7d008409-1162-4dc3-a8b1-760bd1f3330e)

# Credits 
ChessBoard was written by John Eriksson (wmjoers) and released under Gnu Public Licence (GPL)
ChessBoard is an implementation of the laws of chess. It validates moves, tests game states, tests for checkmate etc.

Original code is available here:
https://chess.fortherapy.co.uk/home/software/chessboard/

# References
Project of electronic chessboard based on this great site with many knowledge about creating your own chessboard.
Currently site is not available in original shape, you can reach only this resource:
https://chess.fortherapy.co.uk/home/software/chessboard/

Lichess API manual
https://lichess.org/api

