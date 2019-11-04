
import vrep
import time
import math
import threading 
import numpy as np
import sys

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
n=0.95

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


def bot1(clientID):
	sensor = []
	for i in range(16):
		sensor.append(0)
	x=-5
	y=-5
	lm1=1
	rm1=1
	print("Entered bot1")
	time.sleep(1)
	bot_num = 1
	t = time.time()
	robot = 'Pioneer_p3dx'
	returnCode,leftMotor =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_leftMotor',vrep.simx_opmode_blocking)
	returnCode,rightMotor =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_rightMotor',vrep.simx_opmode_blocking)
	returnCode,robot_handle =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx',vrep.simx_opmode_blocking)

	#for i in range(16):
		# s_name = robot + "_ultrasonicSensor" + str(i)
		# errorcode, sensor[i] = vrep.simxGetObjectHandle(clientID,s_name,vrep.simx_opmode_blocking)

	returnCode, ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_streaming)
	time.sleep(delay)
	# returnCode, pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_blocking)
	returnCode, pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_streaming)
	returnCode, ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
	time.sleep(delay)
	returnCode, pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
	time.sleep(delay)
	print(time.time() - t)
	print('pos = ',pos)
	slope1 = (y-pos[1])/(x-pos[0])

	theta = math.atan(slope1)
	if x<pos[0] and y>pos[1]:
		theta = 3.14+theta
	if x<pos[0] and y<pos[1]:
		theta = -3.14+theta
		
	

	print('theta=',theta)
	print('ori=',ori[2])

	while(ori[2] < 0.95*theta or ori[2] > 1.05*theta):
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
	while(pos[0]<x*n   and  pos[1]<y*n):
		returnCode,pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
		time.sleep(delay)
		returnCode,ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
		time.sleep(delay)
		# v_left, v_right = check_collision(sensor)
		returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, v_left, vrep.simx_opmode_streaming)
		returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, v_right, vrep.simx_opmode_streaming)

		# prin(pos,ori)
		# print("pos = ", pos)
		# print("Actual slope = ", ac_slope)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, 0,vrep.simx_opmode_streaming)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, 0,vrep.simx_opmode_streaming)
	# time.sleep(0.5)
	time.sleep(delay)
	print("bot1 reached target")






if __name__ == "__main__": 
	vrep.simxFinish(-1) # just in case, close all opened connections
	clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP
	if clientID!=-1:
	    print ('Connected to remote API server')
	else:
		print ('Failed connecting to remote API server')
		sys.exit()
	bot1(clientID)
