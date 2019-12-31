import cv2
import numpy as np



def nothing(x):
    pass
cv2.namedWindow('result')

cv2.createTrackbar('h', 'result',0,179,nothing)
cv2.createTrackbar('s', 'result',0,255,nothing)
cv2.createTrackbar('v', 'result',0,255,nothing)
cv2.createTrackbar('h1', 'result',0,179,nothing)
cv2.createTrackbar('s1', 'result',0,255,nothing)
cv2.createTrackbar('v1', 'result',0,255,nothing)

i=0
def main(raspi=False):
    cap = cv2.VideoCapture(0)
    while(1):
        global i
        _, frame = cap.read()
        frame=cv2.resize(frame,(400,300))
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

        h = cv2.getTrackbarPos('h','result')
        s = cv2.getTrackbarPos('s','result')
        v = cv2.getTrackbarPos('v','result')
        h1 = cv2.getTrackbarPos('h1','result')
        s1 = cv2.getTrackbarPos('s1','result')
        v1 = cv2.getTrackbarPos('v1','result')


        lower_blue = np.array([h,s,v])
        upper_blue = np.array([h1,s1,v1])

        mask = cv2.inRange(hsv,lower_blue, upper_blue)

        result = cv2.bitwise_and(frame,frame,mask = mask)

        cv2.imshow('img',result)
        cv2.imwrite('/home/pi/Pictures/img'+str(i)+'.jpg',frame)
        i=i+1
        k = cv2.waitKey(10)

    cap.release()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

