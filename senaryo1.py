#!/usr/bin/env python3

#  Senario 1
#Libraries
import RPi.GPIO as GPIO
import time
import logging 
import random
import os

os.remove(r'/tmp/omxplayerdbus.root')
os.remove(r'/tmp/omxplayerdbus.root.pid')
time.sleep(3)

LOG_FILENAME='logs.log'
logging.basicConfig(format='%(asctime)s (%(lineno)d) %(message)s',filename='logs',
level=logging.DEBUG)

from omxplayer.player import OMXPlayer
from omxplayer.keys import PAUSE,REWIND 
from pathlib import Path

from trigger import trigger
from settings import lostInTime,delay,_debug,m_width,m_height

player_log = logging.getLogger("Player 1")
try:
    player = OMXPlayer("/home/pi/Projects/MuzeApp/media.mp4", 
                          args=['--loop','-o', 'both','--no-osd','--win','0 0 '+m_width+' '+m_height]
                        ,dbus_name='org.mpris.MediaPlayer2.omxplayer1'+str(random.randint(0,99)))
except Exception as e:
    print(e)
player.playEvent += lambda _: player_log.info("Play")
player.pauseEvent += lambda _: player_log.info("Pause")
player.stopEvent += lambda _: player_log.info("Stop")
time.sleep(5)
player.pause()
player.set_alpha(0)

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER    = 23
GPIO_ECHO       = 24



#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

measurements = []
lostDetectionCounterMax = lostInTime*1000 / delay   #Iteration counts for deactivation
is_playing = False
if __name__ == '__main__':
    try:
        LD_Counter= 0
        while True:
            if(trigger(measurements,GPIO_TRIGGER,GPIO_ECHO)):
                LD_Counter = lostDetectionCounterMax
            
            if( LD_Counter ):
                LD_Counter -=1
                print ("LD_Counter = %d " % LD_Counter) if _debug else True
                if(not is_playing):
                    player.set_alpha(100 if _debug else 255 ) 
                    player.play()
                    print ("Video has started")
                    is_playing = True
            else:
                if(is_playing):
                    print ("Video has stopped")
                    player.pause()
                    player.set_alpha(0)
                    player.set_position(0)
                    is_playing = False



    
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
        logging.debug("Measurement stopped by User")
        player.quit()

    except Exception as e:
        print (e)
        logging.debug(e)
        GPIO.cleanup()
        player.quit()
