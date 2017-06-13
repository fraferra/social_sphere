"""
pin connections:
R-B-G-Y
(B)lack to Anode
B(LED) -> 8	ground
R(LED) -> 12	red
G(LED) -> 16	green
Y(LED) -> 22	blue

"""

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

GPIO.setup(8,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)

GPIO.output(8,GPIO.HIGH)
GPIO.output(12,GPIO.LOW)
GPIO.output(16,GPIO.HIGH)
GPIO.output(22,GPIO.HIGH)

sleep(5)

GPIO.cleanup()
