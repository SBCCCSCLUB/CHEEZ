#!/usr/bin/python3
# 2017-05-26 by scharette
# very basic example of AL5 + Python

# obtain required libraries
import serial

# create and open a serial port
sp = serial.Serial('/dev/ttyUSB0', 9600)

# set the arm to default centered position
sp.write("#0 P1500\r".encode())
sp.write("#1 P1500\r".encode())
sp.write("#2 P1500\r".encode())
sp.write("#3 P1500\r".encode())
sp.write("#4 P1500\r".encode())
sp.write("#5 P1500\r".encode())

while input("continue?(y) ") == "y":
    motor = str(input("motor number(0..5): "))
    sp.write(("#" + motor + " P" + str(input("Pos " + motor + ": ")) + "\r").encode())

# Set all motors to idle/unpowered (pulse = 0)
print("< Idling motors... >")
for i in range(0,6):
    print(("#" + str(i) + " P" + str(0) + "\r").encode())
    sp.write(("#" + str(i) + " P" + str(0) + "\r").encode())
print("< Done >")

