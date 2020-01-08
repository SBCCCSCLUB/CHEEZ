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
        self.root = tk.Tk()
        self.image_array = [[None for i in range(8)] for j in range(8)]
        for rank_row_index in range(7, -1, -1):
            for file_column_index in range(8):
                image_name = "chessPieces/"
                # is there a piece on the tile?
                if self.this_board.board_array[rank_row_index][file_column_index] is not None:
                    # which piece?
                    image_name += self.this_board.board_array[rank_row_index][file_column_index].FEN.lower()
                    # which color piece?
                    if self.this_board.board_array[rank_row_index][file_column_index].FEN.islower():
                        image_name += "d"
                    else:
                        image_name += "l"
                # what color is the tile?
                if (file_column_index + rank_row_index) % 2 != 0:
                    image_name += "l"
                else:
                    image_name += "d"
                # place the tile (and piece)
                image_name += ".gif"
                self.image_array[rank_row_index][file_column_index] = tk.PhotoImage(file=image_name)
                label = tk.Label(image=self.image_array[rank_row_index][file_column_index])
                label.place(x=100*rank_row_index, y=100*file_column_index)


board = ChessBoard.ChessBoard("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1")
GUI = ChessGUI(board)

root = tk.Tk()

root.mainloop()
