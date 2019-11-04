import vrep
import time
import math
import threading 
import numpy as np
import sys

def get_target_pos(clientID):
	returnCode,robot_handle =vrep.simxGetObjectHandle(clientID,'Cuboid',vrep.simx_opmode_blocking)
	returnCode, pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_streaming)
	time.sleep(0.5)
	returnCode, pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
	time.sleep(0.2)
	coordinate = [pos[0], pos[1]]
	# print("bot " + str(bot_num)+ str(pos))
	return coordinate



def get_bot_pos(clientID, bot_num):
	returnCode,robot_handle =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx#'+str(bot_num),vrep.simx_opmode_blocking)
	returnCode, pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_streaming)
	time.sleep(0.5)
	returnCode, pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
	time.sleep(0.2)
	returnCode, pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
	time.sleep(0.5)
	coordinate = [pos[0], pos[1]]
	print("bot " + str(bot_num)+ str(pos))
	return coordinate


class particle(object):
	"""docstring for particle"""
	def __init__(self, clientID, num):

		self.path = []
		self.bot = get_bot_pos(clientID, num)
		self.loc = [self.bot[0] + first_step, self.bot[1] + first_step]



	

	def update_local(self, bot, loc, dest):
		if distance(bot, dest) > distance(loc, dest):
			return loc
		else:
			return bot
	def limit_space(self, coor):
		x,y = coor[0], coor[1]
		x = np.clip(x, x_min, x_max)
		y = np.clip(y, y_min, y_max)
		return(x,y)

g = 1.5
l = 2

pi = 3.14
###number of iterations
count = 500


###space design
row = 100
column = 100

x_min = 0.5
x_max = 10
y_min = 0.5
y_max = 10

min_band = 0.95
max_band = 1.05

### frame movement

x_frame = 0
y_frame = 0

delay = 0.05
n=1.05

grid = np.zeros((row, column))
# print(grid)
dest = [5,5]
first_step = 1
#########PID const
kp=10  #2
kd=0.02
ki=0.005
sample_time=delay
le=0
er=0


def distance(coor, dest):
		# print(coor,dest)
		x,y = coor[0] - x_frame, coor[1] - y_frame

		g = (coor[0] - dest[0])**2 + (coor[1] - dest[1])**2
		d = int(math.sqrt(g))
		# d = (x**2 + y - 11)**2 + (x + y**2 -7)**2
		# d = math.sin(3*pi*x)**2 + ((x-1)**2)*(x+math.sin(3*pi*y)**2) + ((y-1)**2)*(1+math.sin(2*pi*y)**2)
		# print("d = ",d)
		return abs(d)



def glob(a,b,c,d,e):
		x = [[distance(a,dest),a],[distance(b,dest), b],[distance(c,dest),c], [distance(d,dest),d], [distance(e,dest),e] ]
		y = min(x)
		return y[1]

def next(bot, glo, loc):
	###int on x,y was removed
	x = (bot[0]+g*np.random.uniform(0,1)*(glo[0]- bot[0]) + l*np.random.uniform(0,1)*(loc[0] - bot[0])) + np.random.uniform(-0.5,0.5)
	y = (bot[1]+g*np.random.uniform(0,1)*(glo[1]- bot[1]) + l*np.random.uniform(0,1)*(loc[1] - bot[1])) + np.random.uniform(-0.5,0.5)
	
	if x > row -1:
		x = row -1
	if y > column -1:
		y = column -1
	next_step = [x,y]
	# print("next_step = ", next_step)
	return next_step

def check_collision(sensor):
	maxd=0.5   ###clearance from the obstacle
	mind=0.2
	detect=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	braitenbergL=[-0.2,-0.4,-0.6,-0.8,-1,-1.2,-1.4,-1.6, 1.6,1.4,1.2,1,0.8,0.6,0.4,0.2]
	braitenbergR=[-1.6,-1.4,-1.2,-1,-0.8,-0.6,-0.4,-0.2, 0.2,0.4,0.6,0.8,1,1.2,1.4,1.6]
	# braitenbergL=[-0.2,-0.4,-0.6,-0.8,-1,-1.2,-1.4,-1.6, 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
	# braitenbergR=[-1.6,-1.4,-1.2,-1,-0.8,-0.6,-0.4,-0.2, 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
	v = 0.5  ###motor speed
	for i in range(16):

		Code,State,Point,ObjectHandle,SurfaceNormalVector=vrep.simxReadProximitySensor(clientID,sensor[i],vrep.simx_opmode_streaming)
		Code,State,Point,ObjectHandle,SurfaceNormalVector=vrep.simxReadProximitySensor(clientID,sensor[i],vrep.simx_opmode_buffer)
		# time.sleep(0.1)
		# detect[i] = 0
		# print("point = ",Point)
		# dist = math.sqrt(Point[0]**2 + Point[1]**2 + Point[2]**2)
		dist = math.sqrt(Point[0]**2 + Point[2]**2)

		# if (dist < maxd and State != 1):
		if ((State != 0) and (dist < maxd)):
			# print("yes %d",i)
			# print("dist x ,z ",Point[0], Point[2])
			if(dist < mind):
				dist = mind
			detect[i] = 1 - ((dist - mind)/(maxd - mind))
		else:
			detect[i] = 0
	v_left = v
	v_right = v

	for i in range(16):
		v_left = v_left + braitenbergL[i] * detect[i]
		v_right = v_right + braitenbergR[i] * detect[i]
	return v_left, v_right



global v1,v2,v3,v4,v5

def velocity(v):
	if(v<0.005):
		return 1

def compare():
	if(velocity(v1)&velocity(v2)&velocity(v3)&velocity(v4)&velocity(v5)):
		return 1


def pid(ori,theta):
	global er
	global le
	e=ori - theta
	p=kp*e
	er=er+e*sample_time
	i=ki*er
	de = le-e/sample_time
	le=e
	d = kd*de
	pid= p+i+d
	return(pid)
 
def prin(pos,ori):
	if returnCode==0:
		print (pos)
		print ("Angle= ", ori[2])

def bot1(clientID, target):
	sensor = []
	for i in range(16):
		sensor.append(0)
	x, y = target
	lm1=1
	rm1=1
	# global v1
	flag=0
	print("Entered bot1")
	time.sleep(1)
	bot_num = 1
	t = time.time()
	robot = 'Pioneer_p3dx'
	returnCode,leftMotor =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_leftMotor#'+str(bot_num),vrep.simx_opmode_blocking)
	returnCode,rightMotor =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_rightMotor#'+ str(bot_num),vrep.simx_opmode_blocking)
	returnCode,robot_handle =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx#'+str(bot_num),vrep.simx_opmode_blocking)

	for i in range(16):
		s_name = robot + "_ultrasonicSensor" + str(i) + '#' + str(bot_num)
		errorcode, sensor[i] = vrep.simxGetObjectHandle(clientID,s_name,vrep.simx_opmode_blocking)

	returnCode, ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_streaming)
	time.sleep(delay)
	# returnCode, pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_blocking)
	returnCode, pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_streaming)
	returnCode, ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
	time.sleep(delay)
	returnCode, pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
	time.sleep(delay)
	print(time.time() - t)
	# print('pos = ',pos)
	slope1 = (y-pos[1])/(x-pos[0])
	theta = math.atan(slope1)
	if x<pos[0] and y>pos[1]:
		theta = 3.14+theta
	if x<pos[0] and y<pos[1]:
		theta = -3.14+theta
	# print('theta=',theta)
	# print('ori=',ori[2])

	while(ori[2] < min_band*theta or ori[2] > max_band*theta):
		omega=pid(ori[2],theta)
		lm=omega*0.0275
		rm=-lm
		returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, lm,vrep.simx_opmode_streaming)
		returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, rm,vrep.simx_opmode_streaming)
		returnCode, ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
		time.sleep(delay)
		# print('ori=',ori[2])

	returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, 0,vrep.simx_opmode_streaming)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, 0,vrep.simx_opmode_streaming)
	time.sleep(delay)
	# time.sleep(0.5)
	print("Entered bot1 done ori")
	while(pos[0]<x*n   and  pos[1]<y*n ):
		returnCode,pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
		time.sleep(delay)
		returnCode,ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
		time.sleep(delay)
		v_left, v_right = check_collision(sensor)
		returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, v_left, vrep.simx_opmode_streaming)
		returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, v_right, vrep.simx_opmode_streaming)
		# v1 = v_left
		# flag=compare()
		# prin(pos,ori)
		# print("pos = ", pos)
		# print("Actual slope = ", ac_slope)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, 0,vrep.simx_opmode_streaming)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, 0,vrep.simx_opmode_streaming)
	# time.sleep(0.5)
	time.sleep(delay)
	print("bot1 reached target")

def bot2(clientID, target):
	sensor = []
	for i in range(16):
		sensor.append(0)
	x, y = target
	lm1=1
	rm1=1
	# global v2
	flag=0
	print("Entered bot2")
	time.sleep(1)
	bot_num = 2
	t = time.time()
	robot = 'Pioneer_p3dx'
	returnCode,leftMotor =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_leftMotor#'+str(bot_num),vrep.simx_opmode_blocking)
	returnCode,rightMotor =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_rightMotor#'+ str(bot_num),vrep.simx_opmode_blocking)
	returnCode,robot_handle =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx#'+str(bot_num),vrep.simx_opmode_blocking)

	for i in range(16):
		s_name = robot + "_ultrasonicSensor" + str(i) + '#' + str(bot_num)
		errorcode, sensor[i] = vrep.simxGetObjectHandle(clientID,s_name,vrep.simx_opmode_blocking)

	returnCode, ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_streaming)
	time.sleep(delay)
	# returnCode, pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_blocking)
	returnCode, pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_streaming)
	returnCode, ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
	time.sleep(delay)
	returnCode, pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
	time.sleep(delay)
	print(time.time() - t)
	# print('pos = ',pos)
	slope1 = (y-pos[1])/(x-pos[0])
	theta = math.atan(slope1)
	if x<pos[0] and y>pos[1]:
		theta = 3.14+theta
	if x<pos[0] and y<pos[1]:
		theta = -3.14+theta
	# print('theta=',theta)
	# print('ori=',ori[2])

	while(ori[2] < min_band*theta or ori[2] > max_band*theta):
		omega=pid(ori[2],theta)
		lm=omega*0.0275
		rm=-lm
		returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, lm,vrep.simx_opmode_streaming)
		returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, rm,vrep.simx_opmode_streaming)
		returnCode, ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
		time.sleep(delay)
		# print('ori=',ori[2])


	returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, 0,vrep.simx_opmode_streaming)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, 0,vrep.simx_opmode_streaming)
	time.sleep(delay)
	# time.sleep(0.5)
	print("Entered bot2 done ori")
	while(pos[0]<x*n   and  pos[1]<y*n ):
		returnCode,pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
		time.sleep(delay)
		returnCode,ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
		time.sleep(delay)
		v_left, v_right = check_collision(sensor)
		returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, v_left, vrep.simx_opmode_streaming)
		returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, v_right, vrep.simx_opmode_streaming)
		# v2 = v_left
		# flag=compare()
		# prin(pos,ori)
		# print("pos = ", pos)
		# print("Actual slope = ", ac_slope)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, 0,vrep.simx_opmode_streaming)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, 0,vrep.simx_opmode_streaming)
	# time.sleep(0.5)
	time.sleep(delay)
	print("bot2 reached target")

def bot3(clientID, target):
	sensor = []
	for i in range(16):
		sensor.append(0)
	x, y = target
	lm=1
	rm=1
	# global v3
	flag=0
	bot_num = 3
	print("Entered bot3")
	robot = 'Pioneer_p3dx'
	time.sleep(1)
	t = time.time()
	returnCode,leftMotor =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_leftMotor#'+str(bot_num),vrep.simx_opmode_blocking)
	returnCode,rightMotor =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_rightMotor#'+ str(bot_num),vrep.simx_opmode_blocking)
	returnCode,robot_handle =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx#'+str(bot_num),vrep.simx_opmode_blocking)

	for i in range(16):
		s_name = robot + "_ultrasonicSensor" + str(i) + '#' + str(bot_num)
		errorcode, sensor[i] = vrep.simxGetObjectHandle(clientID,s_name,vrep.simx_opmode_blocking)

	returnCode, ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_streaming)
	time.sleep(delay)
	# returnCode, pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_blocking)
	returnCode, pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_streaming)
	returnCode, ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
	time.sleep(delay)
	returnCode, pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
	time.sleep(delay)

	# print('pos = ',pos)
	slope = (y-pos[1])/(x-pos[0])
	theta = math.atan(slope)
	if x<pos[0] and y>pos[1]:
		theta = 3.14+theta
	if x<pos[0] and y<pos[1]:
		theta = -3.14+theta
	# print('theta=',theta)
	# print('ori=',ori[2])
	# input()
	while(ori[2] < min_band*theta or ori[2] > max_band*theta):
		omega=pid(ori[2],theta)
		lm=omega*0.0275
		rm=-lm
		returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, lm,vrep.simx_opmode_streaming)
		returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, rm,vrep.simx_opmode_streaming)
		returnCode, ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
		time.sleep(delay)
		# print('ori=',ori[2])

	returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, 0,vrep.simx_opmode_streaming)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, 0,vrep.simx_opmode_streaming)
	time.sleep(delay)
	# time.sleep(0.5)
	print("Entered bot3 done ori")
	while(pos[0]<x*n   and  pos[1]<y*n):
		returnCode,pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
		time.sleep(delay)
		returnCode,ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
		time.sleep(delay)
		v_left, v_right = check_collision(sensor)
		returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, v_left,vrep.simx_opmode_streaming)
		returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, v_right,vrep.simx_opmode_streaming)
		# print('pos = ',pos)
		# prin(pos,ori)
		# print("Init slope = ", slope)
		# print("Actual slope = ", ac_slope)
		# v1 = v_left
		# flag=compare() 
	returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, 0,vrep.simx_opmode_streaming)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, 0,vrep.simx_opmode_streaming)
	time.sleep(delay)
	# time.sleep(0.5)
	print("bot3 reached target")

def bot4(clientID, target):
	sensor = []
	for i in range(16):
		sensor.append(0)
	x, y = target
	lm=1
	rm=1
	# global v4
	flag=0
	bot_num = 4
	print("Entered bot4")
	robot = 'Pioneer_p3dx'
	time.sleep(1)
	t = time.time()
	returnCode,leftMotor =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_leftMotor#'+str(bot_num),vrep.simx_opmode_blocking)
	returnCode,rightMotor =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_rightMotor#'+ str(bot_num),vrep.simx_opmode_blocking)
	returnCode,robot_handle =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx#'+str(bot_num),vrep.simx_opmode_blocking)

	for i in range(16):
		s_name = robot + "_ultrasonicSensor" + str(i) + '#' + str(bot_num)
		errorcode, sensor[i] = vrep.simxGetObjectHandle(clientID,s_name,vrep.simx_opmode_blocking)

	returnCode, ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_streaming)
	time.sleep(delay)
	# returnCode, pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_blocking)
	returnCode, pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_streaming)
	returnCode, ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
	time.sleep(delay)
	returnCode, pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
	time.sleep(delay)

	# print('pos = ',pos)
	slope = (y-pos[1])/(x-pos[0])
	theta = math.atan(slope)
	if x<pos[0] and y>pos[1]:
		theta = 3.14+theta
	if x<pos[0] and y<pos[1]:
		theta = -3.14+theta
	# print('theta=',theta)
	# print('ori=',ori[2])
	# input()
	while(ori[2] < min_band*theta or ori[2] > max_band*theta):
		omega=pid(ori[2],theta)
		lm=omega*0.0275
		rm=-lm
		returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, lm,vrep.simx_opmode_streaming)
		returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, rm,vrep.simx_opmode_streaming)
		returnCode, ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
		time.sleep(delay)
		# print('ori=',ori[2])
	returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, 0,vrep.simx_opmode_streaming)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, 0,vrep.simx_opmode_streaming)
	time.sleep(delay)
	# time.sleep(0.5)
	print("Entered bot4 done ori")
	while(pos[0]<x*n   and  pos[1]<y*n ):
		returnCode,pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
		time.sleep(delay)
		returnCode,ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
		time.sleep(delay)
		v_left, v_right = check_collision(sensor)
		returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, v_left,vrep.simx_opmode_streaming)
		returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, v_right,vrep.simx_opmode_streaming)
		# print('pos = ',pos)
		# v1 = v_left
		# flag=compare()
		# prin(pos,ori)
		# print("Init slope = ", slope)
		# print("Actual slope = ", ac_slope)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, 0,vrep.simx_opmode_streaming)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, 0,vrep.simx_opmode_streaming)
	time.sleep(delay)
	# time.sleep(0.5)
	print("bot4 reached target")

def bot5(clientID, target):
	sensor = []
	for i in range(16):
		sensor.append(0)
	x, y = target
	lm=1
	rm=1
	# global v5
	flag=0
	bot_num = 5
	prev_pos = []
	print("Entered bot5")
	robot = 'Pioneer_p3dx'
	time.sleep(1)
	t = time.time()
	returnCode,leftMotor =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_leftMotor#'+str(bot_num),vrep.simx_opmode_blocking)
	returnCode,rightMotor =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_rightMotor#'+ str(bot_num),vrep.simx_opmode_blocking)
	returnCode,robot_handle =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx#'+str(bot_num),vrep.simx_opmode_blocking)

	for i in range(16):
		s_name = robot + "_ultrasonicSensor" + str(i) + '#' + str(bot_num)
		errorcode, sensor[i] = vrep.simxGetObjectHandle(clientID,s_name,vrep.simx_opmode_blocking)

	returnCode, ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_streaming)
	time.sleep(delay)
	# returnCode, pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_blocking)
	returnCode, pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_streaming)
	returnCode, ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
	time.sleep(delay)
	returnCode, pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
	time.sleep(delay)

	# print('pos = ',pos)
	slope = (y-pos[1])/(x-pos[0])
	theta = math.atan(slope)

	# theta = math.atan(slope1)
	if x<pos[0] and y>pos[1]:
		theta = 3.14+theta
	if x<pos[0] and y<pos[1]:
		theta = -3.14+theta
		
	prev_pos = [pos[0],pos[1]]
	# print('theta=',theta)
	# print('ori=',ori[2])
	# input()
	while(ori[2] < min_band*theta or ori[2] > max_band*theta):
		omega=pid(ori[2],theta)
		lm=omega*0.0275
		rm=-lm
		returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, lm,vrep.simx_opmode_streaming)
		returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, rm,vrep.simx_opmode_streaming)
		returnCode, ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
		time.sleep(delay)
		# print('ori=',ori[2])

	returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, 0,vrep.simx_opmode_streaming)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, 0,vrep.simx_opmode_streaming)
	time.sleep(delay)
	# time.sleep(0.5)
	print("Entered bot5 done ori")
	while(pos[0]<x*n   and  pos[1]<y*n):
		returnCode,pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
		time.sleep(delay)
		returnCode,ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
		time.sleep(delay)
		v_left, v_right = check_collision(sensor)
		returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, v_left,vrep.simx_opmode_streaming)
		returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, v_right,vrep.simx_opmode_streaming)


		# print('pos = ',pos)
		# v1 = v_left
		# falg=compare()
		# prin(pos,ori)
		# print("Init slope = ", slope)
		# print("Actual slope = ", ac_slope)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, 0,vrep.simx_opmode_streaming)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, 0,vrep.simx_opmode_streaming)
	time.sleep(delay)
	# time.sleep(0.5)
	print("bot5 reached target")

def pso_thread():

	global count
	global g_des
	global dest
	while(count>0) :
	
		# while((c.bot!=dest) and (b.bot !=dest) and (c.bot !=dest)):
		
		###global
		g_des = glob(a.loc,b.loc,c.loc,d.loc,e.loc)
		
		###storing location
		a.path.append(a.bot)
		b.path.append(b.bot)
		c.path.append(c.bot)
		d.path.append(d.bot)
		e.path.append(e.bot)


		###finding next step
		a_next = next(a.bot, g_des, a.loc )
		b_next = next(b.bot, g_des, b.loc )
		c_next = next(c.bot, g_des, c.loc )
		d_next = next(d.bot, g_des, d.loc )
		e_next = next(e.bot, g_des, e.loc )

		###limting the space
		a_next = a.limit_space(a_next)
		b_next = b.limit_space(b_next)
		c_next = c.limit_space(c_next)
		d_next = d.limit_space(d_next)
		e_next = e.limit_space(e_next)

	
		###mov next
		a.bot = a_next
		b.bot = b_next
		c.bot = c_next
		d.bot = d_next
		e.bot = e_next
		## udating new local decision
		a.loc = a.update_local(a.bot, a.loc, dest)
		b.loc = b.update_local(b.bot, b.loc, dest)
		c.loc = c.update_local(c.bot, c.loc, dest)
		d.loc = d.update_local(d.bot, d.loc, dest)
		e.loc = e.update_local(e.bot, e.loc, dest)

	
		count = count -1
		# input()
		if count%30 == 0:
			t1 = threading.Thread(target=bot1, args=(clientID, a.bot))
			t2 = threading.Thread(target=bot2, args=(clientID, b.bot))
			t3 = threading.Thread(target=bot3, args=(clientID, c.bot))
			t4 = threading.Thread(target=bot4, args=(clientID, d.bot))
			t5 = threading.Thread(target=bot5, args=(clientID, e.bot))
			t1.start()
			t2.start()
			t3.start()
			t4.start()
			t5.start()
			t1.join()
			t2.join()
			t3.join()
			t4.join()
			t5.join()
			####new bot location
			a.bot=get_bot_pos(clientID,1)
			b.bot=get_bot_pos(clientID,2)
			c.bot=get_bot_pos(clientID,3)
			d.bot=get_bot_pos(clientID,4)
			e.bot=get_bot_pos(clientID,5)
			####new target location
			
		# print("Done")


if __name__ == "__main__": 
	vrep.simxFinish(-1) # just in case, close all opened connections
	clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP
	if clientID!=-1:
	    print ('Connected to remote API server')
	else:
		print ('Failed connecting to remote API server')
		sys.exit()
	a = particle(clientID, 1)
	b = particle(clientID, 2)
	c = particle(clientID, 3)
	d = particle(clientID, 4)
	e = particle(clientID, 5)
	dest = get_target_pos(clientID)
	# sys.exit()
	pso_thread()