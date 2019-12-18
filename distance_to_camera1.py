# USAGE
# python distance_to_camera.py

# import the necessary packages
from imutils import paths
import numpy as np
import imutils
import cv2

lowerBound=np.array([94,130, 60])
upperBound=np.array([126, 255,190])


cam= cv2.VideoCapture(0)
kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))

def find_marker(image):
        image=cv2.resize(image,(340,220))
	# convert the image to grayscale, blur it, and detect edges
	#convert BGR to HSV
        imgHSV= cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        cv2.imshow("image", imgHSV)
        # create the Mask
        mask=cv2.inRange(imgHSV,lowerBound,upperBound)
        #morphology
        maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
        maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

        maskFinal=maskClose
        conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        
        cv2.drawContours(image,conts,-1,(255,0,0),3)
        for i in range(len(conts)):
            x,y,w,h=cv2.boundingRect(conts[i])
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255), 2)
            cv2.imshow("image1", image)
            return  cv2.boundingRect(conts[i])

def distance_to_camera(knownWidth, focalLength, perWidth):
	# compute and return the distance from the maker to the camera
	return (knownWidth * focalLength) / perWidth

# initialize the known distance from the camera to the object, which
# in this case is 24 inches
KNOWN_DISTANCE = 30

# initialize the known object width, which in this case, the piece of
# paper is 12 inches wide
KNOWN_WIDTH = 6

# load the furst image that contains an object that is KNOWN TO BE 2 feet
# from our camera, then find the paper marker in the image, and initialize
# the focal length
image = cv2.imread("images/26mm_focal.jpeg")
marker = find_marker(image)
print (marker)
focalLength = (marker[2] * KNOWN_DISTANCE) / KNOWN_WIDTH
print(focalLength)
# loop over the images
while (True):
	# load the image, find the marker in the image, then compute the
	# distance to the marker from the camera
	#ret, image = cam.read()
	image = cv2.imread("images/15cm_26mm_focal.jpeg")
	marker = find_marker(image)
	print (marker)
	inches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[2])

	# draw a bounding box around the image and display it
	#box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
	#box = np.int0(box)
	#cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
	#cv2.putText(image, "%.2fft" % (inches / 12),
		#(image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
		#2.0, (0, 255, 0), 3)
	print("cm =", inches)
	#cv2.imshow("image", image)
	#cv2.waitKey(0)
