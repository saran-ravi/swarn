import socket
from threading import Thread


##global var
host = ''  #IP_ADD of the bot
port = 5000



def next_action(global_data):
	print("Global data frame",global_data)
	return

def Transmit(host, port):
	global local_data, global_data
	i = 0

	while True:   ### change according to the end condition
		s = socket.socket()
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((host, port))
		s.listen(5)
		conn, add = s.accept()

		if i == 0:
			conn.send(str.encode(local_data))
			i = 1
		else:
			global_data = conn.recv(1024).decode()
			next_action(global_data)
			i = 0
		s.close()

if __name__ == "__main__":

	comm_thread = Thread(target = Transmit, args = (host, port))
	comm_thread.start()
	comm_thread.join()
