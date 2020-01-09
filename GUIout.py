#!/usr/bin/python3
"""NOT GUI interface of UCI, Instead actual GUI to represent board digitally

use for debugging and digital representation of the board without arm
basically it shows the ChessBoard Object's current state
(and therefore what the computer thinks is happening), graphically

TODO write it"""
from tkinter import PhotoImage
from typing import List

import time
import ChessBoard
import tkinter as tk
from PIL import Image, ImageTk


class ChessGUI:
    tk_photo_image_array: []

    def __init__(self, chess_board: ChessBoard.ChessBoard):
        # set the board
        self.this_board = chess_board
        # for holding PhotoImages
        self.tk_photo_image_array = []

        # create the window at full size
        self.root = tk.Tk()
        self.root.geometry("832x832")
        self.root.title = "CHEEZ"

        self.root.update()

        self.populate_squares()

    def get_image_name(self, rank_row_index, file_column_index):
        image_name: str = "chessPieces/"
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
        return image_name

    def populate_squares(self, event=""):
        self.root.unbind_all("<Configure>")
        new_tk_photo_image_array = []
        rank_row_index: int
        for rank_row_index in range(7, -1, -1):
            file_column_index: int
            for file_column_index in range(8):
                image_name = self.get_image_name(rank_row_index, file_column_index)
                image = Image.open(image_name)
                xsize = int(self.root.winfo_width() / 8) - 4
                ysize = int(self.root.winfo_height() / 8) - 4
                if (xsize != 100) or (ysize != 100):
                    image = image.resize((xsize, ysize))
                tk_photo_image: PhotoImage = ImageTk.PhotoImage(image)
                new_tk_photo_image_array.append(tk_photo_image)
                label = tk.Label(self.root, image=tk_photo_image)
                label.grid(row=rank_row_index, column=file_column_index)
            # self.root.update()
        self.tk_photo_image_array = new_tk_photo_image_array
        print(event)
        self.root.update()
        time.sleep(1)
        self.root.bind("<Configure>", self.populate_squares)


board = ChessBoard.ChessBoard("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1")
GUI = ChessGUI(board)

root = tk.Tk()

root.mainloop()
