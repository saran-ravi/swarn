import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

encoder1=3
encoder2=5
count=0
cou=0
GPIO.setup(encoder1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(encoder2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setwarnings(False)
c=2*3.14*3.2
dist = c*0.25
rpm=0
h=0
start1, start2 = 0,0
stop=0
d = 0
def encoder_reading(channel):
    global h, start,stop
    global d
    if (channel == encoder1):
        
        global rpm
        if(h==0):
            start1=time.time()
            h=1
        global count
        count=count+1
        print(count)
        if(count>=5 and h==1):
            stop1=time.time()
            count=0
            h=0
            m1=abs(start1-stop1)
            #print(dist)
            #sp1=(3.14*6.5)/(4*m)
            #sp2=dist/m
            d1 = d1 + dist
            print(d1)
            #print(sp2)
        '''
        if (h == 0):
            start = time.time()
            h=1
        global count
        count= count +1
        if ((time.time()-start) > )
        '''
    elif(channel==encoder2):
        
        global rpm
        if(l==0):
            start2=time.time()
            l=1
        global con
        con=con+1
        print(con)
        if(con>=5 and l==1):
            stop2=time.time()
            con=0
            l=0
            m2=abs(start2-stop2)
            #print(dist)
            ##sp1=(3.14*6.5)/(4*m)
            #sp2=dist/m
            d2 = d2 + dist
            print(d2)
    #print(count)
    #GPIO.input(dt)

GPIO.add_event_detect(encoder1, GPIO.FALLING, callback=encoder_reading)
GPIO.add_event_detect(encoder2, GPIO.RISING, callback=encoder_reading)

if __name__ == '__main__':
    try:
        while True:
            #print("Encoder 1______"+str(rpm))
            #print("Encoder 2______"+str(cou))
            time.sleep(1)
 
        
    except KeyboardInterrupt:
        print("stop")
        GPIO.cleanup()
