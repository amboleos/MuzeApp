
import statistics
import random
import time

from distance import distance
from settings import limit,delay,scan

def trigger(measurements,GPIO_TRIGGER,GPIO_ECHO):
    # Reduce interference posibility with random scan time
    real_delay =random.randrange(int(delay-delay/4),
                                 int(delay+delay/4),
                                 5)
    time.sleep(real_delay/1000)
    
    # Measure raw distance and add to measurements array
    dist = distance(GPIO_TRIGGER,GPIO_ECHO)            
    if(len(measurements) >= scan):
        measurements.pop(0)
    measurements.append(dist)
    
    """ print("Real Delay = %.3f ms" % (real_delay/1000))
    print ("Measured Distance = %.1f cm" % dist)
    print ("Calculated Mean = %.1f cm" % statistics.mean(measurements))
    print ( "Measurements = ",measurements ) """

    # If limit has been passed then trigger action
    if limit > statistics.mean(measurements):
        return True
    else:
        return False