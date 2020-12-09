#Libraries
import RPi.GPIO as GPIO
import time
import logging 

from trigger import trigger


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

measurements=[]

if __name__ == '__main__':
    try:
        
        while True:
            if(trigger(measurements,GPIO_TRIGGER,GPIO_ECHO)):
                pass

            time.sleep(1)
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
        logging.debug("Measurement stopped by User")

    except Exception as e:
        print (e)
        logging.debug(e)
        GPIO.cleanup()
