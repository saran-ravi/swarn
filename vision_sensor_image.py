import vrep
import time
import sys
import numpy as np
import matplotlib.pyplot as plt


delay = 0.5  #######optimum delay is 79 milli secs -- 64x64
vrep.simxFinish(-1)
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)
if clientID != -1:
	print("API connected")

error,cam_handle = vrep.simxGetObjectHandle(clientID,'cam',vrep.simx_opmode_blocking)
print("cam = ",cam_handle)
# time.sleep(delay)
returnCode,resolution,image=vrep.simxGetVisionSensorImage(clientID,cam_handle,0,vrep.simx_opmode_streaming)
time.sleep(delay)
print(returnCode)

# print(len(image), resolution)
for i in range(10):
	returnCode,resolution,image=vrep.simxGetVisionSensorImage(clientID,cam_handle,0,vrep.simx_opmode_buffer)
	time.sleep(delay)
	print(len(image), resolution)
	im = np.array(image,dtype=np.uint8)
	im.resize([resolution[0], resolution[1], 3])
	time.sleep(delay)
	plt.imshow(im,origin = 'lower')
	plt.savefig('bot'+str(i)+'.png')
	time.sleep(delay)