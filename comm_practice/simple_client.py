import socket
s = socket.socket()
port = 9999
host = '192.168.1.240'

s.connect((host, port))
s.send("hello mugil")
s.close
