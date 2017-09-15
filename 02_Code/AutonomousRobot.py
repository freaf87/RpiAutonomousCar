#!/usr/bin/env python()

from threading import Thread
import RPi.GPIO as GPIO
from HCSR04    import HCSR04
from MCP3004   import MCP3004
from TB6612FNG import TB6612FNG
from LED       import LED
import time


class HeartBeat:
    def __init__(self):
        self._running = True
        self.LED = LED()

    def terminate(self):
        self._running = False
        self.LED.destroy()

    def run(self):
        while self._running:
            self.LED.ledOn()
            time.sleep(0.5)
            self.LED.ledOff()
            time.sleep(0.5)

class  LineFollower:
    def __init__(self):
        self._running = True
        #IR Sensor:
        #TODO: Move this to own class
        self.IRLeft  = 27
        self.IRRight = 18
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IRLeft ,GPIO.IN)
        GPIO.setup(self.IRRight,GPIO.IN)
        # Motor Obj
        self._MotorDrive = TB6612FNG()
    def terminate(self):
        self._running = False

    def run(self):
        statusLeft  = False
        statusRight = False
        dc = 3
        print "running..."
        while self._running:
            statusLeft  = bool(GPIO.input(self.IRLeft))
            statusRight = bool(GPIO.input(self.IRRight))
            if statusLeft and statusRight:
                self._MotorDrive.forward(dc)
            elif statusLeft:
                # line on the left => move left
                self._MotorDrive.left(dc)
            elif statusRight:
                # line on the right => move right
                self._MotorDrive.right(dc)

if __name__ == "__main__":

    try:
        Th1 = HeartBeat()
        HeartBeatThread = Thread(target = Th1.run)
        HeartBeatThread.start()

        Th2 = LineFollower()
        RpiAutCarThread = Thread(target = Th2.run)
        RpiAutCarThread.start()

        while True:
            pass
    except KeyboardInterrupt:
        Th1.terminate()
        Th2.terminate()



