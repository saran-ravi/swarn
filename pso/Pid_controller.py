import vrep
import time
import math


def prin(pos,ori):
	if returnCode==0:
		print (pos)
		print ("Angle= ", ori[2])

def stright():
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

x=.5
y=.5
lm=1
rm=1
kp=2
kd=0.02
ki=0.005
sample_time=0.05
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

slope = (x-pos[0])/(y-pos[1])
theta=math.atan(slope)
a=0.99
b=1.02
print(theta)
print(ori[2])
while(ori[2]>b*theta or ori[2]<a*theta):

#	if (ac_slope>=slope):
#		lm=lm+0.3
#		rm=rm-0.3
#	elif(ac_slope<=slope):
#		lm=lm-0.3
#		rm=rm+0.3
	time.sleep(0.05)
	returnCode, ori=vrep.simxGetObjectOrientation(clientID, robot_handle, -1, vrep.simx_opmode_streaming)
	omega=pid(ori[2],theta)
	lm=omega*0.0275
	rm=-lm
	print(ori[2])
	returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, lm,vrep.simx_opmode_streaming)
	returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, rm,vrep.simx_opmode_streaming)
	#print("Init slope = ", slope)
	#print("Actual slope = ", ac_slope)
print("done_with_orientation")

returnCode=vrep.simxSetJointTargetVelocity(clientID, leftMotor, 0,vrep.simx_opmode_streaming)
returnCode=vrep.simxSetJointTargetVelocity(clientID, rightMotor, 0,vrep.simx_opmode_streaming)


