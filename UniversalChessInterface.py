"""This program acts as a Chess GUI interface

TODO Maintains the digital and physical board:
TODO Sends physical commands of the Engine's moves to arm
    TODO Checks that move was successful through computer vision
Reads User move from:
    TODO GUI,
    TODO command line,
    or
    TODO computer vision
TODO Updates GUI representation of any move (User or Engine)
"""

import ChessBoard

board = ChessBoard.ChessBoard()
board.populate_start()
piece = board.delete("e2")
board.add(piece, "e4")

fen = board.export_to_fen()
print(fen)

del board

newBoard = ChessBoard.ChessBoard()
newBoard.setup_from_fen(fen)

newFEN = newBoard.export_to_fen()
print(newFEN)
