"""
A simple Python script to send messages to a sever over Bluetooth
using PyBluez (with Python 2).
"""

import bluetooth
from emotion_classifier import *


serverMACAddress = 'B8:27:EB:B5:14:89'
port = 10
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.settimeout(20)
s.connect((serverMACAddress, port))
while 1:
    print("starting")
    text = get_emotion()# raw_input() # Note change to the old (Python 2) raw_input
    print(text)
    if text == "quit":
        break
    s.send(text)
sock.close()
