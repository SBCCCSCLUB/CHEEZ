"""NOT GUI interface of UCI, Instead actual GUI to represent board digitally

use for debugging and digital representation of the board without arm
basically it shows the ChessBoard Object's current state
(and therefore what the computer thinks is happening), graphically

TODO write it"""

import ChessBoard
import tkinter as tk


class ChessGUI:
    def __init__(self, chess_board: ChessBoard.ChessBoard):
        self.this_board = chess_board
        for row in self.this_board.board_array:
            for square in row:
                if square is not None:
                    print(square.FEN)
                else:
                    print()


board = ChessBoard.ChessBoard()
GUI = ChessGUI(board)

root = tk.Tk()
image = tk.PhotoImage(file="chessPieces/bdd.gif")
label = tk.Label(image=image)
label.place(x=100, y=100)
root.mainloop()
