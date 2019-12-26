"""This file defines the ChessBoard class whose object holds the current position of all pieces

default starts with pieces in standard starting position

TODO write it"""


class ChessBoard:
    """defines chess board digital representation

    :parameter self.board_array is a 2D array of ChessPiece in the form [rank index][file index]
    None indicates there is no piece at the location
    rank = number, file = letter
        rank/file index should not be confused with rank/file as they are 0-7 rather than 1-8/A-H
            Instead, use the available functions
    """
    def __init__(self):
        self.board_array = [[None for i in range(8)] for j in range(8)]

    def populate_start(self):
        """sets up the board with a standard game"""
        # pawns
        for i in range(65, 73):
            self.add_by_rank_and_file(ChessPawn('w'), 2, chr(i))
            self.add_by_rank_and_file(ChessPawn('b'), 7, chr(i))
        # bishops
        self.add_by_rank_and_file(ChessBishop('w'), 1, 'c')
        self.add_by_rank_and_file(ChessBishop('w'), 1, 'f')
        self.add_by_rank_and_file(ChessBishop('b'), 8, 'c')
        self.add_by_rank_and_file(ChessBishop('b'), 8, 'f')
        # knights
        self.add_by_rank_and_file(ChessKnight('w'), 1, 'b')
        self.add_by_rank_and_file(ChessKnight('w'), 1, 'g')
        self.add_by_rank_and_file(ChessKnight('b'), 8, 'b')
        self.add_by_rank_and_file(ChessKnight('b'), 8, 'g')
        # rooks
        self.add_by_rank_and_file(ChessRook('w'), 1, 'a')
        self.add_by_rank_and_file(ChessRook('w'), 1, 'h')
        self.add_by_rank_and_file(ChessRook('b'), 8, 'a')
        self.add_by_rank_and_file(ChessRook('b'), 8, 'h')
        # queens
        self.add_by_rank_and_file(ChessQueen('w'), 1, 'd')
        self.add_by_rank_and_file(ChessQueen('b'), 8, 'd')
        # kings
        self.add_by_rank_and_file(ChessKing('w'), 1, 'e')
        self.add_by_rank_and_file(ChessKing('b'), 8, 'e')

    def export_to_board_representation(self):
        return_string = ""
        for rank_row_index in range(7, -1, -1):
            for file_column_index in range(8):
                if self.board_array[rank_row_index][file_column_index] is not None:
                    piece_fen = self.board_array[rank_row_index][file_column_index].FEN
                    return_string += piece_fen
                elif (file_column_index + rank_row_index) % 2 != 0:
                    return_string += " "
                else:
                    return_string += "█"
            return_string += "\r\n"
        return return_string

    def export_to_fen(self):
        """:returns string of Forsyth–Edwards Notation

        TODO finish"""
        return_string = ""
        return return_string

    def access_by_rank_and_file(self, rank, file):
        return self.board_array[rank - 1][(ord(file) % 32) - 1]

    def access(self, file_first_str):
        return self.access_by_rank_and_file(int(str(file_first_str)[1]), str(file_first_str)[0])

    def add_by_rank_and_file(self, piece, rank, file):
        self.board_array[rank - 1][(ord(file) % 32) - 1] = piece

    def add(self, piece, file_first_str):
        self.add_by_rank_and_file(piece, int(str(file_first_str)[1]), str(file_first_str)[0])

    def delete_by_rank_and_file(self, rank, file):
        return_val = self.access_by_rank_and_file(rank, file)
        self.add_by_rank_and_file(None, rank, file)
        return return_val

    def delete(self, file_first_str):
        return self.delete_by_rank_and_file(int(str(file_first_str)[1]), str(file_first_str)[0])


class ChessPiece:
    """defines parent piece

    TODO Change height_mm to mm height of pieces
    """
    def __init__(self, color, height_mm, value):
        self.color = color
        self.height_mm = height_mm
        self.value = value = value


class ChessPawn(ChessPiece):
    # TODO Change height_mm to mm height of pawn
    def __init__(self, color):
        super().__init__(color, 20.0, 1)
        if color == 'w':
            self.FEN = 'P'
        elif color == 'b':
            self.FEN = 'p'


class ChessBishop(ChessPiece):
    # TODO Change height_mm to mm height of bishop
    def __init__(self, color):
        super().__init__(color, 35.0, 3)
        if color == 'w':
            self.FEN = 'B'
        elif color == 'b':
            self.FEN = 'b'


class ChessKnight(ChessPiece):
    # TODO Change height_mm to mm height of knight
    def __init__(self, color):
        super().__init__(color, 30.0, 3)
        if color == 'w':
            self.FEN = 'N'
        elif color == 'b':
            self.FEN = 'n'


class ChessRook(ChessPiece):
    # TODO Change height_mm to mm height of rook
    def __init__(self, color):
        super().__init__(color, 35.0, 5)
        if color == 'w':
            self.FEN = 'R'
        elif color == 'b':
            self.FEN = 'r'


class ChessQueen(ChessPiece):
    # TODO Change height_mm to mm height of queen
    def __init__(self, color):
        super().__init__(color, 40.0, 10)
        if color == 'w':
            self.FEN = 'Q'
        elif color == 'b':
            self.FEN = 'q'


class ChessKing(ChessPiece):
    # TODO Change height_mm to mm height of king
    def __init__(self, color):
        super().__init__(color, 40.0, 100)
        if color == 'w':
            self.FEN = 'K'
        elif color == 'b':
            self.FEN = 'k'
