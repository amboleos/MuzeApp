#  Senario 2
#Libraries
import RPi.GPIO as GPIO
import time
import logging 
from omxplayer.player import OMXPlayer
from omxplayer.keys import PAUSE,REWIND 
from pathlib import Path
from screeninfo import get_monitors

from settings import _debug,startDelay

for monitor in get_monitors():
    print(str(monitor))

LOG_FILENAME='logs.log'
logging.basicConfig(format='%(asctime)s (%(lineno)d) %(message)s',filename='logs',
level=logging.DEBUG)

VIDEO_1_PATH = Path("../media.wav")
player_log = logging.getLogger("Player 1")
player = OMXPlayer(VIDEO_1_PATH, args=['--loop','-o', 'both','--no-osd','--win','0 0 ' + str(monitor.width) + ' ' + str(monitor.height)],
        dbus_name='org.mpris.MediaPlayer2.omxplayer1')
player.playEvent += lambda _: player_log.info("Play")
player.pauseEvent += lambda _: player_log.info("Pause")
player.stopEvent += lambda _: player_log.info("Stop")
player.action(PAUSE)
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

            position = player.position()
            print (last_position,position)
            if( last_position - position >1):
                print ("Video has stopped")
                player.pause()
                player.set_position(0.1)
                is_playing = False
            last_position  =position

    
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
