import vrep
import time
import math


def prin(pos,ori):
	if returnCode==0:
		print (pos)
		print ("Angle= ", ori[2])

def straight():
	returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, 1,vrep.simx_opmode_streaming)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, 1,vrep.simx_opmode_streaming)


vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP
if clientID!=-1:
    print ('Connected to remote API server')
else:
	print ('Failed connecting to remote API server')

# returnCode =vrep.simxStartSimulation(clientID,vrep.simx_opmode_oneshot)
returnCode,leftMotor =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_leftMotor',vrep.simx_opmode_blocking)
returnCode,rightMotor =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_rightMotor',vrep.simx_opmode_blocking)
returnCode,robot_handle =vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx',vrep.simx_opmode_blocking)
returnCode, pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_streaming)
returnCode, ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_streaming)
x=0.5
y=5
lm=1
rm=1

returnCode, ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
slope = (y-pos[1])/(x-pos[0])
theta = math.atan(slope)
print('theta=',theta)
print('ori=',ori[2])

if (theta<0):
	lm=0
	rm=1
	t = -1*0.06*theta/(2*3.14*0.0275)
	print('t=',t)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, 0,vrep.simx_opmode_streaming)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, 1,vrep.simx_opmode_streaming)
	time.sleep(t)
	lm=0
	rm=0
	returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, 0,vrep.simx_opmode_streaming)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, 0,vrep.simx_opmode_streaming)
	time.sleep(0.5)
elif (theta>0):
	lm=1
	rm=0
	t = 1*0.06*theta/(2*3.14*0.0275)
	print('t=',t)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, 1,vrep.simx_opmode_streaming)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, 0,vrep.simx_opmode_streaming)
	time.sleep(t)
	lm=0
	rm=0
	returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, 0,vrep.simx_opmode_streaming)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, 0,vrep.simx_opmode_streaming)
	time.sleep(0.5)

returnCode, ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
print ('ori=',ori[2])
'''
while(pos[0]<5.3   and  pos[1]<5.3):
	ac_slope = (x-pos[0])/(y-pos[1])
	if (ac_slope>=slope):
		lm=lm+0.3
		rm=rm-0.3
	elif(ac_slope<=slope):
		lm=lm-0.3
		rm=rm+0.3
	returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, lm,vrep.simx_opmode_streaming)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, rm,vrep.simx_opmode_streaming)
	lm=1
	rm=1
	returnCode,pos=vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
	returnCode,ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
	# prin()
	print("Init slope = ", slope)
	print("Actual slope = ", ac_slope)
returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, 0,vrep.simx_opmode_streaming)
returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, 0,vrep.simx_opmode_streaming)
	
'''
