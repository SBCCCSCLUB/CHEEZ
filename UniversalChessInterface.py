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

print(board.export_to_board_representation())

piece = board.delete("e2")
board.add(piece, "e4")

fen = board.export_to_fen()
print(fen)
print(board.export_to_board_representation())

del board

newBoard = ChessBoard.ChessBoard(fen)

newFEN = newBoard.export_to_fen()
print(newFEN)
print(newBoard.export_to_board_representation())
