#!/usr/bin/env python3

#  Senario 2
#Libraries
import RPi.GPIO as GPIO
import time
import logging 
import random
import os

try:
    os.remove(r'/tmp/omxplayerdbus.root')
    os.remove(r'/tmp/omxplayerdbus.root.pid')
except:
    pass
time.sleep(3)

LOG_FILENAME='logs.log'
logging.basicConfig(format='%(asctime)s (%(lineno)d) %(message)s',filename='logs',
level=logging.DEBUG)

from omxplayer.player import OMXPlayer
from omxplayer.keys import PAUSE,REWIND 
from pathlib import Path

from trigger import trigger
from settings import lostInTime,delay,_debug,m_width,limit,scan,startDelay,m_width,m_height

player_log = logging.getLogger("Player 1")
try:
    player = OMXPlayer("/home/pi/Projects/MuzeApp/media.wav", 
                          args=['--loop','--vol',volume,'-o', 'both','--no-osd','--win','0 0 '+m_width+' '+m_height]
                        ,dbus_name='org.mpris.MediaPlayer2.omxplayer1'+str(random.randint(0,99)))
except Exception as e:
    print(e)
player.playEvent += lambda _: player_log.info("Play")
player.pauseEvent += lambda _: player_log.info("Pause")
player.stopEvent += lambda _: player_log.info("Stop")
time.sleep(5)
player.pause()

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER    = 23
GPIO_ECHO       = 24
GPIO_BUTTON     = 4



#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_BUTTON, GPIO.IN)

is_playing = False
last_position = 0
if __name__ == '__main__':
    try:
        LD_Counter= 0
        while True:
            time.sleep(0.05)

            if(GPIO.input(GPIO_BUTTON) == GPIO.HIGH):
                time.sleep(0.1)
                if(GPIO.input(GPIO_BUTTON) == GPIO.HIGH):
                    if(not is_playing):
                        time.sleep(startDelay)
                        player.play()
                        print ("Video has started")
                        time.sleep(1.1)
                        is_playing = True
                        
            
            if(GPIO.input(GPIO_BUTTON) == GPIO.LOW):
                time.sleep(0.1)
                if(GPIO.input(GPIO_BUTTON) == GPIO.LOW):        
                    if(is_playing):
                        print ("Video has stopped")
                        player.pause()
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
        # logging.debug(e)
        GPIO.cleanup()
        player.quit()
