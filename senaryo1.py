#  Senario 1
#Libraries
import RPi.GPIO as GPIO
import time
import logging 
from omxplayer.player import OMXPlayer
from omxplayer.keys import PAUSE,REWIND 
from pathlib import Path
from screeninfo import get_monitors

from trigger import trigger
from settings import lostInTime,delay,_debug

for monitor in get_monitors():
    print(str(monitor))

LOG_FILENAME='logs.log'
logging.basicConfig(format='%(asctime)s (%(lineno)d) %(message)s',filename='logs',
level=logging.INFO)

VIDEO_1_PATH = Path("../media.mp4")
player_log = logging.getLogger("Player 1")
player = OMXPlayer(VIDEO_1_PATH, args=['--loop','-o', 'both','--no-osd','--win','0 0 ' + str(monitor.width) + ' ' + str(monitor.height)],
        dbus_name='org.mpris.MediaPlayer2.omxplayer1')
player.playEvent += lambda _: player_log.info("Play")
player.pauseEvent += lambda _: player_log.info("Pause")
player.stopEvent += lambda _: player_log.info("Stop")
player.action(PAUSE)
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
        # logging.debug(e)
        GPIO.cleanup()
        player.quit()
