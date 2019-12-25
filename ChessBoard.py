"""This file defines the ChessBoard class whose object holds the current position of all pieces

default starts with pieces in standard starting position

TODO write it"""
import Pieces


class ChessBoard:
    def __init__(self):
        self.board_array = [[None]*8]*8
