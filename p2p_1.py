import vrep
import time
import math
import threading 


delay = 0.1

def check_collision(sensor):
	maxd=0.5   ###clearance from the obstacle
	mind=0.2
	detect=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	braitenbergL=[-0.2,-0.4,-0.6,-0.8,-1,-1.2,-1.4,-1.6, 1.6,1.4,1.2,1,0.8,0.6,0.4,0.2]
	braitenbergR=[-1.6,-1.4,-1.2,-1,-0.8,-0.6,-0.4,-0.2, 0.2,0.4,0.6,0.8,1,1.2,1.4,1.6]
	# braitenbergL=[-0.2,-0.4,-0.6,-0.8,-1,-1.2,-1.4,-1.6, 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
	# braitenbergR=[-1.6,-1.4,-1.2,-1,-0.8,-0.6,-0.4,-0.2, 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
	v = 1  ###motor speed from the bot function
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


def prin(pos,ori):
	if returnCode==0:
		print (pos)
		print ("Angle= ", ori[2])

def straight():
	returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, 1,vrep.simx_opmode_streaming)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, 1,vrep.simx_opmode_streaming)

def bot1(clientID):
	sensor = []
	for i in range(16):
		sensor.append(0)
	x=5
	y=5
	lm=1
	rm=1
	print("ENtered bot1")
	robot = 'Pioneer_p3dx'
	time.sleep(1)
	t = time.time()
	returnCode,leftMotor =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_leftMotor',vrep.simx_opmode_blocking)
	returnCode,rightMotor =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_rightMotor',vrep.simx_opmode_blocking)
	returnCode,robot_handle =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx',vrep.simx_opmode_blocking)

	for i in range(16):
		s_name = robot + "_ultrasonicSensor" + str(i)
		errorcode, sensor[i] = vrep.simxGetObjectHandle(clientID,s_name,vrep.simx_opmode_blocking)

	returnCode, ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_streaming)
	time.sleep(delay)
	# returnCode, pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_blocking)
	returnCode, pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_streaming)
	returnCode, ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
	time.sleep(delay)
	returnCode, pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
	time.sleep(delay)

	print('pos = ',pos)
	slope = (y-pos[1])/(x-pos[0])
	theta = math.atan(slope)
	print('theta=',theta)
	print('ori=',ori[2])
	# input()
	while(ori[2] < 0.95*theta or ori[2] > 1.05*theta):
		returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, -0.2,vrep.simx_opmode_streaming)
		returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, 0.2,vrep.simx_opmode_streaming)
		returnCode, ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
		time.sleep(delay)
		print('ori1=',ori[2])

	returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, 0,vrep.simx_opmode_streaming)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, 0,vrep.simx_opmode_streaming)
	time.sleep(delay)
	# time.sleep(0.5)
	print("ENtered bot1 done ori")
	while(pos[0]<x*1.05   and  pos[1]<y*1.05):
		returnCode,pos=vrep.simxGetObjectPosition(clientID, robot_handle, 1, vrep.simx_opmode_buffer)
		time.sleep(delay)
		returnCode,ori=vrep.simxGetObjectOrientation(clientID, robot_handle, 1, vrep.simx_opmode_buffer)
		time.sleep(delay)
		v_left, v_right = check_collision(sensor)
		returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, v_left,vrep.simx_opmode_streaming)
		returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, v_right,vrep.simx_opmode_streaming)
		print('pos = ',pos)
		# prin(pos,ori)
		# print("Init slope = ", slope)
		# print("Actual slope = ", ac_slope)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, 0,vrep.simx_opmode_streaming)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, 0,vrep.simx_opmode_streaming)
	time.sleep(delay)
	# time.sleep(0.5)
	print("ENtered bot1 reached target")

def bot2(clientID):
	sensor = []
	for i in range(16):
		sensor.append(0)
	x=5
	y=5
	lm1=1
	rm1=1
	print("ENtered bot2")
	time.sleep(1)
	t = time.time()
	robot = 'Pioneer_p3dx1'
	returnCode,leftMotor1 =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_leftMotor1',vrep.simx_opmode_blocking)
	returnCode,rightMotor1 =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_rightMotor1',vrep.simx_opmode_blocking)
	returnCode,robot_handle1 =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx1',vrep.simx_opmode_blocking)


	for i in range(16):
		s_name = robot + "_ultrasonicSensor" + str(i)
		errorcode, sensor[i] = vrep.simxGetObjectHandle(clientID,s_name,vrep.simx_opmode_blocking)

	returnCode, ori1=vrep.simxGetObjectOrientation(clientID, robot_handle1, -1, vrep.simx_opmode_streaming)
	time.sleep(delay)
	# returnCode, pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_blocking)
	returnCode, pos1=vrep.simxGetObjectPosition(clientID, robot_handle1, -1, vrep.simx_opmode_streaming)
	returnCode, ori1=vrep.simxGetObjectOrientation(clientID, robot_handle1, -1, vrep.simx_opmode_buffer)
	time.sleep(delay)
	returnCode, pos1=vrep.simxGetObjectPosition(clientID, robot_handle1, -1, vrep.simx_opmode_buffer)
	time.sleep(delay)
	print(time.time() - t)
	print('pos = ',pos1)
	slope1 = (y-pos1[1])/(x-pos1[0])
	theta1 = math.atan(slope1)
	print('theta=',theta1)
	print('ori=',ori1[2])

	while(ori1[2] < 0.95*theta1 or ori1[2] > 1.05*theta1):
		returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor1, -0.2,vrep.simx_opmode_streaming)
		returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor1, 0.2,vrep.simx_opmode_streaming)

		returnCode, ori1=vrep.simxGetObjectOrientation(clientID, robot_handle1, -1, vrep.simx_opmode_buffer)
		time.sleep(delay)
		# print('ori1=',ori1[2])

	returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor1, 0,vrep.simx_opmode_streaming)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor1, 0,vrep.simx_opmode_streaming)
	time.sleep(delay)
	# time.sleep(0.5)
	print("ENtered bot2 done ori")
	while(pos1[0]<x*1.05   and  pos1[1]<y*1.05):
		returnCode,pos1=vrep.simxGetObjectPosition(clientID, robot_handle1, 1, vrep.simx_opmode_buffer)
		time.sleep(delay)
		returnCode,ori1=vrep.simxGetObjectOrientation(clientID, robot_handle1, 1, vrep.simx_opmode_buffer)
		time.sleep(delay)
		v_left, v_right = check_collision(sensor)
		returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor1, v_left, vrep.simx_opmode_streaming)
		returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor1, v_right, vrep.simx_opmode_streaming)

		# prin(pos,ori)
		# print("pos = ", pos1)
		# print("Actual slope = ", ac_slope)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor1, 0,vrep.simx_opmode_streaming)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor1, 0,vrep.simx_opmode_streaming)
	# time.sleep(0.5)
	time.sleep(delay)
	print("ENtered bot2 reached target")





if __name__ == "__main__": 
	vrep.simxFinish(-1) # just in case, close all opened connections
	clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP
	if clientID!=-1:
	    print ('Connected to remote API server')
	else:
		print ('Failed connecting to remote API server')
	t1 = threading.Thread(target=bot1, args=(clientID,))
	t2 = threading.Thread(target=bot2, args=(clientID,))
	t1.start()
	t2.start()
	t1.join()
	t2.join()
	print("Done")