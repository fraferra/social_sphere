"""
A simple Python script to receive messages from a client over
Bluetooth using PyBluez (with Python 2).
"""

"""
pin connections:
R-B-G-Y
(B)lack to Anode
R(LED) -> 8     ground
B(LED) -> 12    red
G(LED) -> 16    green
Y(LED) -> 22    blue

"""

import bluetooth
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

GPIO.setup(8,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)

GPIO.output(8,GPIO.LOW)
GPIO.output(12,GPIO.HIGH)
GPIO.output(16,GPIO.LOW)
GPIO.output(22,GPIO.LOW)

hostMACAddress = 'B8:27:EB:B5:14:89' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 10
backlog = 10
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
s.listen(backlog)
try:
    client, clientInfo = s.accept()
    while 1:
        data = client.recv(size)
	"""
	while data == null:
            GPIO.output(8,GPIO.LOW)
            GPIO.output(12,GPIO.HIGH)
            GPIO.output(16,GPIO.LOW)
            GPIO.output(22,GPIO.LOW)
	    sleep(1)
	"""
        if data == "neutral":
	    print(data)
	    GPIO.output(8,GPIO.HIGH)
	    GPIO.output(12,GPIO.HIGH)
	    GPIO.output(16,GPIO.HIGH)
	    GPIO.output(22,GPIO.LOW)
	elif data == "angry":
            print(data)
            GPIO.output(8,GPIO.LOW)
            GPIO.output(12,GPIO.HIGH)
            GPIO.output(16,GPIO.HIGH)
            GPIO.output(22,GPIO.HIGH)
	elif data == "sad":
            print(data)
            GPIO.output(8,GPIO.LOW)
            GPIO.output(12,GPIO.HIGH)
            GPIO.output(16,GPIO.LOW)
            GPIO.output(22,GPIO.HIGH)
	elif data == "happy":
            print(data)
            GPIO.output(8,GPIO.HIGH)
            GPIO.output(12,GPIO.HIGH)
            GPIO.output(16,GPIO.LOW)
            GPIO.output(22,GPIO.HIGH)
	else:
            GPIO.output(8,GPIO.HIGH)
            GPIO.output(12,GPIO.HIGH)
            GPIO.output(16,GPIO.HIGH)
            GPIO.output(22,GPIO.HIGH)
	    
except:
    print("Closing socket")
    s.close()
    GPIO.cleanup()



