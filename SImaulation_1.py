import vrep
import sys
import matplotlib.pyplot as plt
import numpy as np
import time
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP

if clientID!=-1:
    print ('Connected to remote API server')
else:
	print('connection not sucessful')
	sys.exit('NOT CONNECTED')


''' FOR CONTROLLING MOTOR POSITION       '''
'''
error,left_motor_handle=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_leftMotor',vrep.simx_opmode_oneshot_wait)
error,right_motor_handle=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_rightMotor',vrep.simx_opmode_oneshot_wait)

#error=vrep.simxSetObjectOrientation(clientID,left_motor_handle,-1,[-9.79874403839176e-10, 4.70646899231042e-09, -8.384952617217917e-14],vrep.simx_opmode_blocking)
#error=vrep.simxSetObjectOrientation(clientID,right_motor_handle,-1,[-9.79874403839176e-10, 4.70646899231042e-09, -8.384952617217917e-14],vrep.simx_opmode_blocking)

error=vrep.simxSetJointTargetVelocity(clientID,left_motor_handle, 1,vrep.simx_opmode_streaming)
error=vrep.simxSetJointTargetVelocity(clientID,right_motor_handle,0,vrep.simx_opmode_streaming)
print(error)
time.sleep(t)
error=vrep.simxSetJointTargetVelocity(clientID,left_motor_handle, 0,vrep.simx_opmode_streaming)
error=vrep.simxSetJointTargetVelocity(clientID,right_motor_handle,0,vrep.simx_opmode_streaming)
'''
#function to read sensor
'''
error,sensor1=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor1',vrep.simx_opmode_blocking)
print(sensor1)
print(error)
error,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=vrep.simxReadProximitySensor(clientID,sensor1,vrep.simx_opmode_blocking)
error,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=vrep.simxReadProximitySensor(clientID,sensor1,vrep.simx_opmode_buffer)

'''
#CAMERA
'''
error,camhandle=vrep.simxGetObjectHandle(clientID,'cam1',vrep.simx_opmode_blocking)
print(camhandle)
error,resolution,image=vrep.simxGetVisionSensorImage(clientID,camhandle,0, vrep.simx_opmode_blocking)
print(error)
#print(image)
im=np.array(image,dtype=np.uint8)
print(im.shape)
im.resize([resolution[0],resolution[1],3])
print(im.shape)
for r in range(64):
	for c in range(64):
		im[r,c]=im[r,c,1]
#im=im([resolution[0],resolution[1],1])
#plt.plot(im)
plt.show()'''

'''
error,sensor2=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor5',vrep.simx_opmode_blocking)
error,detectionState,detectedPoint1,detectedObjectHandle,detectedSurfaceNormalVector=vrep.simxReadProximitySensor(clientID,sensor2,vrep.simx_opmode_blocking)
print(detectedPoint1)
print(detectionState)
x,y=detectedPoint1
v_des=0.1
om_des=0.1
d=0.06
r_w=0.0275
v_r=(v_des+d*0.5*om_des)
v_l=(v_des-d*0.5*om_des)
error=vrep.simxSetJointTargetVelocity(clientID,left_motor_handle, v_l,vrep.simx_opmode_streaming)
error=vrep.simxSetJointTargetVelocity(clientID,right_motor_handle,v_r,vrep.simx_opmode_streaming)
print(error)
'''

#orientation of bot
'''
error,cubhandle=vrep.simxGetObjectHandle(clientID,'Cuboid',vrep.simx_opmode_streaming)
error,handles,intData,floatData,stringData=vrep.simxGetObjectGroupData(clientID,cubhandle,5,vrep.simx_opmode_blocking)

print(error)
len(stringData)
print((stringData))
print(floatData[6]-floatData[36],floatData[7]-floatData[37],floatData[8]-floatData[38])


error,left_motor_handle=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_leftMotor',vrep.simx_opmode_oneshot_wait)
error,right_motor_handle=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_rightMotor',vrep.simx_opmode_oneshot_wait)

theta=floatData[8]-floatData[38]
t=0.06*theta/(0.0275*2*3.14)
t=int(t)
error=vrep.simxSetJointTargetVelocity(clientID,left_motor_handle, 1,vrep.simx_opmode_streaming)
error=vrep.simxSetJointTargetVelocity(clientID,right_motor_handle,0,vrep.simx_opmode_streaming)
print(error)
time.sleep(t )
error=vrep.simxSetJointTargetVelocity(clientID,left_motor_handle, 0,vrep.simx_opmode_streaming)
error=vrep.simxSetJointTargetVelocity(clientID,right_motor_handle,0,vrep.simx_opmode_streaming)

error=vrep.simxSetJointTargetVelocity(clientID,left_motor_handle,-1,vrep.simx_opmode_streaming)
error=vrep.simxSetJointTargetVelocity(clientID,right_motor_handle,-1,vrep.simx_opmode_streaming)
time.sleep(3)
'''
#3bots
error,cubhandle=vrep.simxGetObjectHandle(clientID,'Cuboid',vrep.simx_opmode_streaming)
#error,handles,intData,floatData,stringData=vrep.simxGetObjectGroupData(clientID,cubhandle,5,vrep.simx_opmode_blocking)
error,handles,intData,floatData1,stringData=vrep.simxGetObjectGroupData(clientID,cubhandle,0,vrep.simx_opmode_blocking)
print(error)
len(stringData)
print(stringData)
'''print(floatData[39]-floatData[36],floatData[40]-floatData[37],floatData[41]-floatData[38])
print(floatData[69]-floatData[36],floatData[70]-floatData[37],floatData[71]-floatData[38])
print(floatData[99]-floatData[36],floatData[100]-floatData[37],floatData[101]-floatData[38])
print(floatData[132]-floatData[36],floatData[133]-floatData[37],floatData[134]-floatData[38])
#print(floatData1[6]-floatData1[36],floatData1[7]-floatData1[37],floatData1[8]-floatData1[38])
'''

error,left_motor_handle=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_leftMotor',vrep.simx_opmode_oneshot_wait)
error,right_motor_handle=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_rightMotor',vrep.simx_opmode_oneshot_wait)
print (floatData[8])
print (floatData[38])
theta=floatData[8]-floatData[38]

if theta<0:
	theta=6.28+theta

t=0.06*theta/(0.0275*2*3.14)
error=vrep.simxSetJointTargetVelocity(clientID,left_motor_handle, 1,vrep.simx_opmode_streaming)
error=vrep.simxSetJointTargetVelocity(clientID,right_motor_handle,0,vrep.simx_opmode_streaming)
time.sleep(t)
error=vrep.simxSetJointTargetVelocity(clientID,left_motor_handle, 0,vrep.simx_opmode_streaming)
error=vrep.simxSetJointTargetVelocity(clientID,right_motor_handle,0,vrep.simx_opmode_streaming)
error,handles,intData,floatData1,stringData=vrep.simxGetObjectGroupData(clientID,cubhandle,0,vrep.simx_opmode_blocking)
print(floatData)
'''
error,left_motor_handle1=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_leftMotor#1',vrep.simx_opmode_oneshot_wait)
error,right_motor_handle1=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_rightMotor#1',vrep.simx_opmode_oneshot_wait)

theta1=floatData[71]-floatData[38]
print (theta1)
print (floatData[71])
print (floatData[38])
if theta1<0:
	theta1=3.14+theta1
t1=0.06*theta1/(0.0275*2*3.14)
print (theta1)

error=vrep.simxSetJointTargetVelocity(clientID,left_motor_handle1, 1,vrep.simx_opmode_streaming)
error=vrep.simxSetJointTargetVelocity(clientID,right_motor_handle1,0,vrep.simx_opmode_streaming)
time.sleep(t1)
error=vrep.simxSetJointTargetVelocity(clientID,left_motor_handle1, 0,vrep.simx_opmode_streaming)
error=vrep.simxSetJointTargetVelocity(clientID,right_motor_handle1,0,vrep.simx_opmode_streaming)
print (floatData[71])

error,left_motor_handle1=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx#1_leftMotor',vrep.simx_opmode_oneshot_wait)
error,right_motor_handle1=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx#1_rightMotor',vrep.simx_opmode_oneshot_wait)

theta1=floatData[71]-floatData[38]
t1=0.06*theta1/(0.0275*2*3.14)
error=vrep.simxSetJointTargetVelocity(clientID,left_motor_handle1, t1,vrep.simx_opmode_streaming)
error=vrep.simxSetJointTargetVelocity(clientID,right_motor_handle1,0,vrep.simx_opmode_streaming)

error,left_motor_handle2=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx#2_leftMotor',vrep.simx_opmode_oneshot_wait)
error,right_motor_handle2=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx#2_rightMotor',vrep.simx_opmode_oneshot_wait)

theta2=floatData[101]-floatData[38]
t2=0.06*theta2/(0.0275*2*3.14)
error=vrep.simxSetJointTargetVelocity(clientID,left_motor_handle2, t2,vrep.simx_opmode_streaming)
error=vrep.simxSetJointTargetVelocity(clientID,right_motor_handle2,0,vrep.simx_opmode_streaming)

error,left_motor_handle3=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx#3_leftMotor',vrep.simx_opmode_oneshot_wait)
error,right_motor_handle3=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx#3_rightMotor',vrep.simx_opmode_oneshot_wait)

theta3=floatData[134]-floatData[38]
t3=0.06*theta3/(0.0275*2*3.14)
error=vrep.simxSetJointTargetVelocity(clientID,left_motor_handle3, t3,vrep.simx_opmode_streaming)
error=vrep.simxSetJointTargetVelocity(clientID,right_motor_handle3,0,vrep.simx_opmode_streaming)
print(error)
'''
time.sleep(1)
print (floatData[8])
#error=vrep.simxSetJointTargetVelocity(clientID,left_motor_handle, 0,vrep.simx_opmode_streaming)
#error=vrep.simxSetJointTargetVelocity(clientID,right_motor_handle,0,vrep.simx_opmode_streaming)

#error=vrep.simxSetJointTargetVelocity(clientID,left_motor_handle,-1,vrep.simx_opmode_streaming)
#error=vrep.simxSetJointTargetVelocity(clientID,right_motor_handle,-1,vrep.simx_opmode_streaming)
#time.sleep(3)   	

