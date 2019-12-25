### PC CLIENT
import socket 
from threading import Thread

host = []
port = []
BOT_COUNT = 3

def process_pos_info(pos_info):
	print(pos_info)
	return



def listen(host, port):
	pos_info = ""

	
	while True:
		
		for bot_id in range(BOT_COUNT):
			s = socket.socket()
			s.connect((host[bot_id], port[bot_id]))
			temp = s.recv(1024).decode()
			pos_info = pos_info + temp
			s.close()

		global_data = process_pos_info(pos_info)
		pos_info = ""

		for bot_id in range(BOT_COUNT):
			s.socket.socket()
			s.connect((host[bot_id], port[bot_id]))
			s.send(str.encode(global_data))
			s.close()

if __name__ == "__main__":

	comm_thread = Thread(target = listen, args = (host, port))
	comm_thread.start()
	comm_thread.join()



