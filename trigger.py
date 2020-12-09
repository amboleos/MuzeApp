
import statistics
import random
import time

from distance import distance
from settings import limit,delay,scan

def trigger(measurements,GPIO_TRIGGER,GPIO_ECHO):
    # Reduce interference posibility with random scan time
    real_delay =random.randrange((delay-delay/4)/1000,
                                 (delay+delay/4)/1000,
                                 0.005)
    time.sleep(real_delay)
    
    # Measure raw distance and add to measurements array
    dist = distance(GPIO_TRIGGER,GPIO_ECHO)            
    if(len(measurements) >= scan):
        measurements.pop(0)
    measurements.append(dist)
    
    Print("Real Delay = %.3f ms",real_delay)
    print ("Measured Distance = %.1f cm" % dist)
    print ("Calculated Mean = %.1f cm" % statistics.mean(measurements))
    print ( "Measurements = ",measurements )

    # If limit has been passed then trigger action
    if limit > statistics.mean(measurements):
        return True
    else:
        return False