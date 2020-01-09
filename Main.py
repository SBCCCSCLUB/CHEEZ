#!/usr/bin/python3
"""This program acts as a Chess Engine

Sends Universal Chess Interface commands to UniversalChessEngine through SYS.stdin"""

import StockfishInterface

interface = StockfishInterface.StockfishInterface(10)
while True:
    moveStr = input("move: ")
    print(moveStr)
    interface.move(moveStr)
