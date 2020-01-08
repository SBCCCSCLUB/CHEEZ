"""NOT GUI interface of UCI, Instead actual GUI to represent board digitally

use for debugging and digital representation of the board without arm
basically it shows the ChessBoard Object's current state
(and therefore what the computer thinks is happening), graphically

TODO write it"""

from Tkinter import Tk, Frame, Canvas
import ImageTk

t = Tk()
t.title("Transparency")

frame = Frame(t)
frame.pack()

canvas = Canvas(frame, bg="black", width=500, height=500)
canvas.pack()

photoimage = ImageTk.PhotoImage(file="chessPieces/bdd.png")
canvas.create_image(150, 150, image=photoimage)

t.mainloop()