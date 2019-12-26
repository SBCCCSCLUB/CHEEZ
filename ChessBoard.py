"""This file defines the ChessBoard class whose object holds the current position of all pieces

default starts with pieces in standard starting position

TODO write it"""


class ChessBoard:
    def __init__(self):
        self.board_array = [[None]*8]*8

    def populate_start(self):
        for i in range(1, 9):
            self.add_by_rankfile(ChessPawn('w'), )
        self.add_by_rankfile()

    def access_by_rankfile(self, rank, file):
        return self.board_array[(ord(rank) % 32) - 1][file - 1]

    def add_by_rankfile(self, piece, rank, file):
        self.board_array[(ord(rank) % 32) - 1][file - 1] = piece

    def delete_by_rankfile(self, rank, file):
        return_val = self.access_by_rankfile(rank, file)
        self.add_by_rankfile(None, rank, file)
        return return_val


class ChessPiece:
    def __init__(self, color, height_mm, value):
        self.color = color
        self.height_mm = height_mm
        self.value = value = value


class ChessPawn(ChessPiece):
    def __init__(self, color):
        super().__init__(color, 20.0, 1)


class ChessBishop(ChessPiece):
    def __init__(self, color):
        super().__init__(color, 35.0, 3)


class ChessKnight(ChessPiece):
    def __init__(self, color):
        super().__init__(color, 30.0, 3)


class ChessRook(ChessPiece):
    def __init__(self, color):
        super().__init__(35.0, 5)


class ChessQueen(ChessPiece):
    def __init__(self, color):
        super().__init__(color, 40.0, 10)


class ChessKing(ChessPiece):
    def __init__(self, color):
        super().__init__(color, 40.0, 100)
