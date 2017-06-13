import socket
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

import socket
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

def angry():
    GPIO.output(8,GPIO.HIGH)
    GPIO.output(12,GPIO.HIGH)
    GPIO.output(16,GPIO.HIGH)
    GPIO.output(22,GPIO.LOW)

def neutral():
    while(1):
        GPIO.output(8,GPIO.LOW)
        GPIO.output(12,GPIO.HIGH)
        GPIO.output(16,GPIO.HIGH)
        GPIO.output(22,GPIO.HIGH)

def happy():
    GPIO.output(8,GPIO.HIGH)
    GPIO.output(12,GPIO.HIGH)
    GPIO.output(16,GPIO.LOW)
    GPIO.output(22,GPIO.HIGH)

def sad():
    GPIO.output(8,GPIO.HIGH)
    GPIO.output(12,GPIO.HIGH)
    GPIO.output(16,GPIO.LOW)
    GPIO.output(22,GPIO.LOW)

def close():
    GPIO.output(8,GPIO.HIGH)
    GPIO.output(12,GPIO.HIGH)
    GPIO.output(16,GPIO.HIGH)
    GPIO.output(22,GPIO.HIGH)

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '' #ip of raspberry pi
    port = 1234
    size = 1024
    s.bind((host, port))

    s.listen(5)
    try:
        c, addr = s.accept()
        print ('Got connection from',addr)
        while True:
            data = c.recv(size)
            if data == "neutral":
                print(data)
                neutral()
            while data == "angry":
                print(data)
                angry()
            while data == "sad":
                print(data)
                sad()
            while data == "happy":
                print(data)
                happy()
            while data != "neutral" or "angry" or "sad" or "happy":
		close()
    except:
        print("Closing socket")
        s.close()
	GPIO.cleanup()
