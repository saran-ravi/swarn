# USAGE
# python distance_to_camera.py

# import the necessary packages
from imutils import paths
import numpy as np
import imutils
import cv2
'''
lower = {'red':(166, 84, 141), 'blue':(97, 100, 117)} 
upper = {'red':(186,255,255), 'blue':(117,255,255)}
'''
lower = {'red':(166, 84, 141)} 
upper = {'red':(186,255,255)}
cam= cv2.VideoCapture(0)
kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))

def find_marker(image):
    #(grabbed, frame) = cam.read()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    for key, value in upper.items():
    
        kernel = np.ones((9,9),np.uint8)
        mask = cv2.inRange(hsv, lower[key], upper[key])
        maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernel)
        mask = maskClose
        cv2.imshow("image2", mask)
        if key == 'red':
            #cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)[-2]
            conts,h = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            #print(cnts)
            cv2.drawContours(image,conts,-1,(255,0,0),3)
            #center = None
            for i in range(len(conts)):
                x,y,w,h=cv2.boundingRect(conts[i])
                cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255), 2)
                return cv2.boundingRect(conts[i])
        if key == 'blue':
            #cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)[-2]
            conts,h = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            #print(cnts)
            cv2.drawContours(image,conts,-1,(255,0,0),3)
            #center = None
            for i in range(len(conts)):
                x,y,w,h=cv2.boundingRect(conts[i])
                cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255), 2)
                return cv2.boundingRect(conts[i])

def distance_to_camera(knownWidth, focalLength, perWidth):
    # compute and return the distance from the maker to the camera
    return (knownWidth * focalLength) / perWidth

# initialize the known distance from the camera to the object, which
# in this case is 24 inches
KNOWN_DISTANCE = 93

# initialize the known object width, which in this case, the piece of
# paper is 12 inches wide
KNOWN_WIDTH = 15

# load the furst image that contains an object that is KNOWN TO BE 2 feet
# from our camera, then find the paper marker in the image, and initialize
# the focal length
img = cv2.imread("images/93_15_red.jpg")
marker = find_marker(img)
#print (marker)
focalLength = (marker[2] * KNOWN_DISTANCE) / KNOWN_WIDTH

print(focalLength)

# loop over the images
while (True):
    # load the image, find the marker in the image, then compute the
    # distance to the marker from the camera
    #ret, image = cam.read()
    image = cv2.imread("images/93_15_red1.jpg")
    marker = find_marker(image)
    while (marker):
                #print (marker)
                inches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[2])

        # draw a bounding box around the image and display it
        #box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
        #box = np.int0(box)
        #cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
        #cv2.putText(image, "%.2fft" % (inches / 12),
                #(image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                #2.0, (0, 255, 0), 3)
                #print("cm =", inches)
                cv2.imshow("image", image)

    cv2.imshow("image", image)
    #cv2.waitKey(0)
