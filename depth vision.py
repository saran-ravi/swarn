import vrep
import time
import sys
import numpy as np
from array import *
print ('Program started')
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)
if clientID!=-1:
    print ('Connected to remote API server')
    returnCode,cam=vrep.simxGetObjectHandle(clientID,'cam',vrep.simx_opmode_oneshot_wait)

    returnCode,resolution,image=vrep.simxGetVisionSensorImage(clientID,cam,0,vrep.simx_opmode_streaming)
    # result,state,packet=vrep.simxGetVisionSensorDepthBuffer(clientID,cam,vrep.simx_opmode_streaming)
    result,State,Packet=vrep.simxReadVisionSensor(clientID,cam,vrep.simx_opmode_streaming)
    returnCode1,resolution1,array1=vrep.simxGetVisionSensorDepthBuffer(clientID,cam,vrep.simx_opmode_streaming)
    i=1
    while(1):

        result,state,packet=vrep.simxReadVisionSensor(clientID,cam,vrep.simx_opmode_buffer)
        #returnCode,resolution,array=vrep.simxGetVisionSensorDepthBuffer(clientID,cam,vrep.simx_opmode_buffer)
        #print(len(array))
        #print(packet[1:])
        if packet:
            d=packet[0]
            bd=packet[1]
            ex=packet[2]
            #x=bd[4];
            #print(d)
            #y=bd[5];
            #print(bd)
            #print(len(ex))
            #print(bd)
            blobcount=bd[0]
            blobcount=int(blobcount)
            datasizeperblob=bd[2]
            #print(datasizeperblob)

            for i in range(1,blobcount):
                x=2+(i-1)*datasizeperblob+2
                x=int(x)
                bloborientation=bd[x]  
                blobposX=bd[x+1] 
                blobposY=bd[x+2] 
                if ex:
                    xin=blobposX*63
                    yin=blobposY*63
                    y=2+4*xin+4*64*yin+1
                    y=int(y)
                    posX=ex[y]
                    posY=ex[y+1]
                    posZ=ex[y+2]
                    dist=ex[y+3] 
                    ''' posX=posX*63 
                    posY=posY*63 
                    posZ=posZ*63'''

        #print(len(packet))
         #   print(packet)
    
                    print("X_value",posX)
                    print("Y_value",posY)
                    print("Z_value",posZ)
                    print("distance_value",dist)
    
        # if packet:
        #     x=packet[5]
        #     y=packet[6]
        #     print("X_value",x)
        #     print("Y_value",y)
        
else :
    print ('Failed connecting to remote API server')
print ('Program ended')
