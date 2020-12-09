#Libraries
import RPi.GPIO as GPIO
import time
import logging 
import subprocess

from trigger import trigger
from settings import lostInTime,delay

LOG_FILENAME='logs.log'
logging.basicConfig(format='%(asctime)s %(message)s',filename='logs',
level=logging.DEBUG)


#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 24



#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

""" 
GPIO_TRIGGER2 = 27
GPIO_ECHO2 = 17
GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
GPIO.setup(GPIO_ECHO2, GPIO.IN)
dist2= distance(GPIO_TRIGGER2,GPIO_ECHO2)
print ("        Measured Distance = %.1f cm" % dist2) 
"""

measurements = []
lostDetectionCounterMax = lostInTime*1000 / delay   #Iteration counts for deactivation
is_playing = False
global myprocess
if __name__ == '__main__':
    try:
        LD_Counter= 0
        while True:
            if(trigger(measurements,GPIO_TRIGGER,GPIO_ECHO)):
                LD_Counter = lostDetectionCounterMax
            
            if( LD_Counter ):
                LD_Counter -=1
                print ("LD_Counter = %d " % LD_Counter)
                if(not is_playing):
                    myprocess = subprocess.Popen(['omxplayer','-b','/home/pi/Desktop/media.mp4'],stdin=subprocess.PIPE)
                    #https://www.raspberrypi.org/documentation/raspbian/applications/omxplayer.md
                    # https://www.raspberrypi.org/forums/viewtopic.php?t=93789
                    # https://raspberrypi.stackexchange.com/questions/8922/how-do-i-display-images-without-starting-x11
                    print ("Video has started")
                    is_playing = True
            else:
                if(is_playing):
                    print ("Video has stopped")
                    is_playing = False
                    myprocess.stdin.write(b"q")



    
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
        logging.debug("Measurement stopped by User")

    # except Exception as e:
    #     print (e)
    #     logging.debug(e)
    #     GPIO.cleanup()
