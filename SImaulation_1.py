import vrep
import sys


vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP

if clientID!=-1:
    print ('Connected to remote API server')
else:
	print('connection not sucessful')
	sys.exit('NOT CONNECTED')

error,left_motor_handle=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_leftMotor',vrep.simx_opmode_oneshot_wait)
error,right_motor_handle=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_rightMotor',vrep.simx_opmode_oneshot_wait)
print(left_motor_handle)
error=vrep.simxSetJointTargetVelocity(clientID,left_motor_handle, 0.2,vrep.simx_opmode_streaming)
#error=vrep.simxSetJointTargetVelocity(clientID,right_motor_handle,0.2,vrep.simx_opmode_streaming)




