import numpy as np
import sys
import os
import cv2
import math
import socket


lower = {'red':(166, 84, 141), 'blue':(97, 100, 117)} 
upper = {'red':(186,255,255), 'blue':(117,255,255)}
KNOWN_DISTANCE = 47
KNOWN_WIDTH = 15
focalLength =0
bot_radius = 1
bot_angle = 1

tx_count = 0
host = ""
port = 9999


def main(raspi=False):
    if raspi:
        os.system('sudo modprobe bcm2835-v4l2')
        
    cam= cv2.VideoCapture(0)

    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)
    conn, add = s.accept()
        
    
    global focalLength 
    focalLength = focallength()
    while (True):
        ret, image = cam.read()
        #image = cv2.imread("images/93_15_red1.jpg")
        #image = cv2.imread("/home/pi/Desktop/93_15_red1.jpg")
        image=cv2.resize(image,(400,300))
        cv2.waitKey(10)
        marker = find_marker(image, conn)
        cv2.imshow("image", image)

def transfer_info(label, data, s):

    if label == "BOT":
        s.send(str.encode(data))

    if label == "OBSTACLE":
        s.send(str.encode(data))


    if label == "TARGET":
        s.send(str.encode(data))









def find_marker(image, s):
    obs_str = ""
    tar_str = ""
    bot_str = ""

    s.send(str.encode("TRACK"))

    bot_str = str(int(bot_radius))+"m"+str(int(bot_angle)) + "r"
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    frame=image
    disr={}
    disb={}
    cv2.putText(frame,".",(200,150),cv2.FONT_HERSHEY_SIMPLEX, 5, (50, 120, 220), 2)
    
    for key, value in upper.items():
        
        kernel = np.ones((9,9),np.uint8)
        mask = cv2.inRange(hsv, lower[key], upper[key])
        maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernel)
        mask = maskClose       

        if key == 'red':
            
            conts,h = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            tx_str = ""
            
            for i in range(len(conts)):

                M = cv2.moments(conts[i])
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.drawContours(frame,conts,-1,(50,150,150),2)
                cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
                cv2.putText(image, "center", (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                x,y,w,h=cv2.boundingRect(conts[i])
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255), 1)
                disr[i]=distance_to_camera(KNOWN_WIDTH, focalLength,w)
                print (disr[i])
                dx=cX-200
                dy=cY-150
                dx1=dx*15/w
                dy1=dy*15/h
                rad1=math.atan(dx1/disr[i])
                deg1=rad1*180/3.14


                rad2=math.atan(dy1/disr[i])
                deg2=rad2*180/3.14
                degree   = int(deg1)
                radius   = int(rad1)

                tar_str = tar_str + str(radius)+"m"+str(radius)+"r"

                #print("red-x = "+str(deg1)+"   \tred-y = "+str(deg2)+"-----target"+str(i))
               
                cv2.putText(frame,"target"+str(i)+"dis - "+str(disr[i]),(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (6, 25, 200), 2)
            
            
                

        elif key == 'blue':
            tx_str = ""

            conts,h = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(frame,conts,-1,(255,0,0),1)

            for i in range(len(conts)):

                
                M = cv2.moments(conts[i])
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.drawContours(frame,conts,-1,(50,150,150),1)
                cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
                cv2.putText(image, "center", (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                x,y,w,h=cv2.boundingRect(conts[i])
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255), 1)
                disb[i]=distance_to_camera(KNOWN_WIDTH, focalLength,w)
                dx=cX-200
                dy=cY-150
                dx1=dx*15/w
                dy1=dy*15/h
                rad1=math.atan(dx1/disb[i])
                deg1=rad1*180/3.14
                rad2=math.atan(dy1/disb[i])
                deg2=rad2*180/3.14
                #print("blue-x = "+str(deg1)+"   \tblue-y = "+str(deg2)+"--------obstacle"+str(i))
                degree   = int(deg1)
                radius   = int(rad1)

                obs_str = obs_str + str(radius)+"m"+str(radius)+"r"
                
                
                cv2.putText(frame,"obstacle"+str(i)+"dis - "+str(disb[i]),(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (6, 25, 200), 2)


    transfer_info("BOT", bot_str, s)
    transfer_info("TARGET", tar_str, s)
    transfer_info("OBSTACLE", obs_str, s)


def distance_to_camera(knownWidth, focalLength, perWidth):
    return (knownWidth * focalLength) / perWidth

def focallength():
    img = cv2.imread("/home/pi/Pictures/img1.jpg")
    img=cv2.resize(img,(400,300))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    frame=img
    kernel = np.ones((9,9),np.uint8)
    mask = cv2.inRange(hsv,(166, 84, 141),(186,255,255))
    maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernel)
    mask = maskClose       
    conts,h = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame,conts,-1,(255,0,0),3)
    #print(len(conts))
    for i in range(len(conts)):
        x,y,w,h=cv2.boundingRect(conts[i])
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255), 2)
        focalLength = (w* KNOWN_DISTANCE) / KNOWN_WIDTH
    return (focalLength)



if __name__ == "__main__":
    main()



