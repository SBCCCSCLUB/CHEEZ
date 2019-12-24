

class ChessPiece:
    def __init__(self, height_mm, value):
        self.height_mm = height_mm
        self.value = value = value


class ChessPawn(ChessPiece):
    def __init__(self):
        super().__init__(20.0, 1)


class ChessBishop(ChessPiece):
    def __init__(self):
        super().__init__(35.0, 3)


class ChessKnight(ChessPiece):
    def __init__(self):
        super().__init__(30.0, 3)


class ChessRook(ChessPiece):
    def __init__(self):
        super().__init__(35.0, 5)


class ChessQueen(ChessPiece):
    def __init__(self):
        super().__init__(40.0, 10)


class ChessKing(ChessPiece):
    def __init__(self):
        super().__init__(40.0, 100)
