#!/usr/bin/env python()
import time
from HCSR04    import HCSR04
from MCP3004   import MCP3004
from TB6612FNG import TB6612FNG
from LED       import LED


def setup():
    pass

def loop(hcsr04, tb6612fng, led):
    distance  = 0
    qualifier = 0
    DutyCycle = 4

    while 1:
        qualifier,distance =  hcsr04.get_averageDistance()
        #print 'Distance = '+ str(distance)
        if qualifier == 1:
            if distance < 20:
                robotDrive.stop()
                time.sleep(0.01)
                robotDrive.reverse(DutyCycle-2)
                time.sleep(0.25)
                robotDrive.left(DutyCycle-2)
                time.sleep(0.25)
                robotDrive.forward(DutyCycle)
            else:
                robotDrive.forward()

        else:
            pass

if __name__ == "__main__":

    try:
        ultrasonic = HCSR04()
        led = LED()
        robotDrive = TB6612FNG()
        loop(ultrasonic, robotDrive, led)
    except KeyboardInterrupt:
        ultrasonic.destroy()

