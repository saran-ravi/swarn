import numpy as np
import imutils
import cv2
import math

lower = {'red':(166, 84, 141), 'blue':(97, 100, 117)} 
upper = {'red':(186,255,255), 'blue':(117,255,255)}
cam= cv2.VideoCapture(0)



def find_marker(image):
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    frame=image
    disr={}
    disb={}
    cv2.putText(frame,".",(350,250),cv2.FONT_HERSHEY_SIMPLEX, 5, (50, 120, 220), 2)
    
    for key, value in upper.items():
        
        kernel = np.ones((9,9),np.uint8)
        mask = cv2.inRange(hsv, lower[key], upper[key])
        maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernel)
        mask = maskClose       

        if key == 'red':
            
            conts,h = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            
            
            for i in range(len(conts)):

                M = cv2.moments(conts[i])
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.drawContours(frame,conts,-1,(255,0,0),3)
                cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
                cv2.putText(image, "center", (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                x,y,w,h=cv2.boundingRect(conts[i])
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255), 2)
                disr[i]=distance_to_camera(KNOWN_WIDTH, focalLength,w)
                
                dx=cX-350
                dy=cY-250
                dx1=dx*15/w
                dy1=dy*15/h
                rad1=math.atan(dx1/disr[i])
                deg1=rad1*180/3.14
                rad2=math.atan(dy1/disr[i])
                deg2=rad2*180/3.14
                print("red-x = "+str(deg1)+"   \tred-y = "+str(deg2)+"-----target"+str(i))
               
                cv2.putText(frame,"target"+str(i)+"dis - "+str(disr[i]),(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (6, 25, 200), 2)
                
                

        elif key == 'blue':

            conts,h = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(frame,conts,-1,(255,0,0),3)

            for i in range(len(conts)):

                
                M = cv2.moments(conts[i])
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.drawContours(frame,conts,-1,(255,0,0),3)
                cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
                cv2.putText(image, "center", (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                x,y,w,h=cv2.boundingRect(conts[i])
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255), 2)
                disb[i]=distance_to_camera(KNOWN_WIDTH, focalLength,w)
                dx=cX-350
                dy=cY-250
                dx1=dx*15/w
                dy1=dy*15/h
                rad1=math.atan(dx1/disb[i])
                deg1=rad1*180/3.14
                rad2=math.atan(dy1/disb[i])
                deg2=rad2*180/3.14
                print("blue-x = "+str(deg1)+"   \tblue-y = "+str(deg2)+"--------obstacle"+str(i))
                
                
                
                cv2.putText(frame,"obstacle"+str(i)+"dis - "+str(disb[i]),(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (6, 25, 200), 2)
                #print(a2)

def distance_to_camera(knownWidth, focalLength, perWidth):
    # compute and return the distance from the maker to the camera
    return (knownWidth * focalLength) / perWidth

# initialize the known distance from the camera to the object, which
# in this case is 24 inches
KNOWN_DISTANCE = 93

# initialize the known object width, which in this case, the piece of
# paper is 12 inches wide
KNOWN_WIDTH = 15

def focallength():
    img = cv2.imread("images/93_15_red.jpg")
    img=cv2.resize(img,(700,500))
    #marker = find_marker(img)
    #cv2.imshow("img", img)
    #print (marker)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    frame=img
    kernel = np.ones((9,9),np.uint8)
    mask = cv2.inRange(hsv,(166, 84, 141),(186,255,255))
    maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernel)
    mask = maskClose       
    conts,h = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame,conts,-1,(255,0,0),3)
    print(len(conts))
    for i in range(len(conts)):
        x,y,w,h=cv2.boundingRect(conts[i])
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255), 2)
        focalLength = (w* KNOWN_DISTANCE) / KNOWN_WIDTH
    return (focalLength)


focalLength = focallength()

while (True):
    # load the image, find the marker in the image, then compute the
    # distance to the marker from the camera
    ret, image = cam.read()
    #image = cv2.imread("images/93_15_red1.jpg")
    image=cv2.resize(image,(700,500))
    cv2.waitKey(500)
    marker = find_marker(image)
    cv2.imshow("image", image)
