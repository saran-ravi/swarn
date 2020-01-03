import socket
from threading import Thread


##global var
host = '192.168.1.138'  #IP_ADD of the bot
port = 9999

def bot_distance():
	d = 10
	return d

def bot_angle():
	d = 14
	return d

def number_of_target():
	d = 5
	return d

def target_distance():
	d = [10,5,7,9,6]
	return d

def target_angle():
	d = [13,21,31,42,62]
	return d

def number_of_obstacle():
	d = 5
	return d

def obstacle_distance():
	d = [9,8,7,6,5]
	return d

def obstacle_angle():
	d = [13,21,31,42,62]
	return d

def next_action(global_data):
	print("Global data frame",global_data)
	return

def Transmit(host, port):
	global local_data, global_data
	i = 0
	k = 0
	td={}
	ta={}
	od={}
	oa={}

	print("a")
	while True:   ### change according to the end condition
		print("d")
		s = socket.socket()
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((host, port))
		s.listen(5)
		conn, add = s.accept()
		

		if i == 0:
			conn.send(str.encode("TRACK"))  # sending mapping data
			print("c")
			botd = bot_distance()					
			bota = bot_angle()
			botp = str(botd)+"m"+str(bota)+"r"
			print(botp)
			conn.send(str.encode(botp))					#sending bot position

			n = number_of_target()
			print(n)
			td = target_distance()
			ta = target_angle()
			print(k)
			tp=""
			while k<n:
			
				tp = tp+str(td[k])+"m"+str(ta[k])+"r"
				k=k+1
			print(tp)
			conn.send(str.encode(tp))					#sending target position

			k=0	
			m = number_of_obstacle()
			od = obstacle_distance()
			oa = obstacle_angle()
			op=""
			while k<n:
				op = op+str(od[k])+"m"+str(oa[k])+"r"
				k=k+1
			print(op)
			conn.send(str.encode(op))					#sending obstacle position

			conn.send(str.encode(local_data))
			i = 1
		else:
			global_data = conn.recv(1024).decode()
			next_action(global_data)
			i = 0
		s.close()

if __name__ == "__main__":
	print("b")
	comm_thread = Thread(target = Transmit, args = (host, port))
	comm_thread.start()
	comm_thread.join()
	Transmit(host, port)
