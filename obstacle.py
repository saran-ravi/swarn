import vrep
import time
import sys
import numpy as np
import matplotlib.pyplot as plt
import math

def check_collision(sensor):
	maxd=0.5   ###clearance from the obstacle
	mind=0.2
	detect=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	braitenbergL=[-0.2,-0.4,-0.6,-0.8,-1,-1.2,-1.4,-1.6, 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
	braitenbergR=[-1.6,-1.4,-1.2,-1,-0.8,-0.6,-0.4,-0.2, 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
	v = 2  ###motor speed
	for i in range(16):

		Code,State,Point,ObjectHandle,SurfaceNormalVector=vrep.simxReadProximitySensor(clientID,sensor[i],vrep.simx_opmode_streaming)
		Code,State,Point,ObjectHandle,SurfaceNormalVector=vrep.simxReadProximitySensor(clientID,sensor[i],vrep.simx_opmode_buffer)
		time.sleep(0.1)
		dist = math.sqrt(Point[0]**2 + Point[1]**2 + Point[2]**2)
		if (dist < maxd):
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


sensor = []
for i in range(16):
	sensor.append(0) 
delay = 0.5  #######optimum delay is 79 milli secs -- 64x64
vrep.simxFinish(-1)
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)
if clientID != -1:
	print("API connected")

robot = 'Pioneer_p3dx'

returnCode,leftMotor1 =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_leftMotor',vrep.simx_opmode_blocking)
returnCode,rightMotor1 =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_rightMotor',vrep.simx_opmode_blocking)
returnCode,robot_handle1 =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx',vrep.simx_opmode_blocking)
# error,bot_handle = vrep.simxGetObjectHandle(clientID,robot,vrep.simx_opmode_blocking)
# print("cam = ",cam_handle)
# print("hello")
# returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor1, 1,vrep.simx_opmode_streaming)
# returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor1, 1,vrep.simx_opmode_streaming)
for i in range(16):
		s_name = robot + "_ultrasonicSensor" + str(i)
		errorcode, sensor[i] = vrep.simxGetObjectHandle(clientID,s_name,vrep.simx_opmode_blocking)

while(True):
	v_left, v_right = check_collision(sensor)

	print(v_left, v_right)

	returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor1, v_left,vrep.simx_opmode_streaming)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor1, v_right,vrep.simx_opmode_streaming)

	# time.sleep(0.2)
# print(bot_hsandle)

# for i in range(1,17):
# 		s_name = robot + "_ultrasonicSensor" + str(i)
# 		errorcode, sensor[i] = vrep.simxGetObjectHandle(clientID,s_name,vrep.simx_opmode_blocking)
# 		print("errorcode = ",errorcode)
# 		returnCode,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=vrep.simxReadProximitySensor(clientID,sensor[i],vrep.simx_opmode_blocking)
# 		returnCode,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=vrep.simxReadProximitySensor(clientID,sensor[i],vrep.simx_opmode_buffer)
# 		time.sleep(0.25)
# 		print(detectedObjectHandle)