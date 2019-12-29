"""This program acts as a Chess Engine

Sends Universal Chess Interface commands to UniversalChessEngine through SYS.stdin"""

import StockfishInterface

interface = StockfishInterface.StockfishInterface(10)
while True:
    interface.move(input("move: "))
