import socket               

s = socket.socket()        
host = '192.168.43.122'# ip of raspberry pi 
port = 12345               
s.connect((host, port))
while 1:
    text = raw_input() # Note change to the old (Python 2) raw_input
    if text == "quit":
        break
    s.send(text)
s.close()
