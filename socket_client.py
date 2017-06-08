import socket               
from emotion_classifier import *

s = socket.socket()        
host = '192.168.43.122'# ip of raspberry pi 
port = 1234        
s.connect((host, port))
while 1:
    text = get_emotion(l = sys.argv)# raw_input() # Note change to the old (Python 2) raw_input

    print(text)# Note change to the old (Python 2) raw_input
    print(type(text))
    if text == "quit":
        break
    s.send(text.encode('utf-8'))
s.close()
