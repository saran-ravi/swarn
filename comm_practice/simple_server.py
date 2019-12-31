#socket program
import socket 

s = socket.socket()

port = '9999'
host = '192.168.1.240'

s.bind((host, port))
s.listen(5)

while  True:
	c, add = s.accept()
	c.send("hello mugil")
	c.close()
