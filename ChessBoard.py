#!/usr/bin/python3
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
    def __init__(self, fen_string="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.turn = None
        self.board_array = [[]]
        self.setup_from_fen(fen_string)

    def populate_start(self):
        """sets up the board with a new standard game"""
        self.setup_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    def setup_from_fen(self, fen_string):
        # build/clear the board
        self.board_array = [[None for i in range(8)] for j in range(8)]
        # parse fen_string
        fen_fields = str(fen_string).split(" ")
        # place the pieces on the board
        self.add_pieces_by_fen_board_field(fen_fields[0])
        # set other fields if they exist
        if len(fen_fields) > 1:
            # set color of next turn
            self.turn = fen_fields[1]
            # set castle ability

    def add_pieces_by_fen_board_field(self, fen_board_field):
        fen_board = fen_board_field.split("/")
        rank_index = 7  # fen_board_index = 7 - rank_index
        while rank_index >= 0:
            file_index = 0
            for character in fen_board[7 - rank_index]:
                if character.isnumeric():
                    file_index += int(character)
                else:
                    self.board_array[rank_index][file_index] = piece_from_fen(character)
                    file_index += 1
            rank_index -= 1

    def export_to_board_representation(self):
        """:returns string of the current board state row by row"""
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
        """:returns string of Forsyth–Edwards Notation of current board state

        TODO finish"""
        return_string = ""
        # board from rank 8 -> 1
        for rank_row_index in range(7, -1, -1):
            none_count = 0
            for file_column_index in range(8):
                if self.board_array[rank_row_index][file_column_index] is not None:
                    if none_count > 0:
                        return_string += str(none_count)
                        none_count = 0
                    return_string += self.board_array[rank_row_index][file_column_index].FEN
                else:
                    none_count += 1
            if none_count > 0:
                return_string += str(none_count)
                none_count -= none_count
            if rank_row_index > 0:
                return_string += "/"
        # active color
        # castling availability
        # en passant target
        # Halfmove clock
        # Fullmove number
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


def piece_from_fen(fen_character):
    """get appropriate piece child object from representative FEN character

    :returns ChessPiece child object"""
    fen_character = str(fen_character[0])
    # find the color
    color = 'b'
    if fen_character.isupper():
        color = 'w'
    # lowercase
    fen_character = fen_character.lower()
    # find the piece
    if fen_character == 'p':
        return ChessPawn(color)
    elif fen_character == 'b':
        return ChessBishop(color)
    elif fen_character == 'n':
        return ChessKnight(color)
    elif fen_character == 'r':
        return ChessRook(color)
    elif fen_character == 'k':
        return ChessKing(color)
    elif fen_character == 'q':
        return ChessQueen(color)
    else:
        return None


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
