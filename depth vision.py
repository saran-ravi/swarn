import vrep
import time
import sys
print ('Program started')
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)
if clientID!=-1:
    print ('Connected to remote API server')
    returnCode,cam=vrep.simxGetObjectHandle(clientID,'cam',vrep.simx_opmode_oneshot_wait)

    returnCode,resolution,image=vrep.simxGetVisionSensorImage(clientID,cam,0,vrep.simx_opmode_streaming)
    # result,state,packet=vrep.simxGetVisionSensorDepthBuffer(clientID,cam,vrep.simx_opmode_streaming)
    result,State,Packet=vrep.simxReadVisionSensor(clientID,cam,vrep.simx_opmode_streaming)
    while(1):

        result,state,packet=vrep.simxReadVisionSensor(clientID,cam,vrep.simx_opmode_buffer)
        print(packet)
        # if packet:
        #     x=packet[5]
        #     y=packet[6]
        #     print("X_value",x)
        #     print("Y_value",y)
        input()
else:
    print ('Failed connecting to remote API server')
print ('Program ended')
