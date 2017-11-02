#!/usr/bin/env python()
import time
from threading import Thread

import RPi.GPIO as GPIO
from HCSR04 import HCSR04  # This is the ultrasonic ranger

from drivers.TB6612FNG import TB6612FNG
from drivers.infrared import InfraredSensor
from drivers.led import LED


class HeartBeat:
    def __init__(self):
        self._running = True
        self._LED = LED()

    def terminate(self):
        self._running = False

    def run(self):
        while self._running:
            self._LED.on()
            time.sleep(0.5)
            self._LED.off()
            time.sleep(0.5)

class AutonomousDrive:
    def __init__(self):
        self._running = True
        self._USonic = HCSR04()
        self._MotorDrive = TB6612FNG()

    def terminate(self):
        self._running = False

    def run(self):
        DutyCycle = 4
        while self._running:
            qualifier,distance =  self._USonic.get_averageDistance()
            if qualifier == 1:
                if distance < 20:
                    self._MotorDrive.stop()
                    time.sleep(0.01)
                    self._MotorDrive.reverse(DutyCycle-2)
                    time.sleep(0.2)
                    self._MotorDrive.left(DutyCycle-2)
                    time.sleep(0.2)
                    self._MotorDrive.forward(DutyCycle)
                else:
                    self._MotorDrive.forward()
            else:
                pass


class LineFollower:
    def __init__(self):
        self._running = True
        self._IR = InfraredSensor()
        self._MotorDrive = TB6612FNG()
        self._USonic = HCSR04()
        self._loopCount = 0
        self._IRNbr = 2

    def terminate(self):
        self._running = False

    def run(self):
        statusLeft  = False
        statusRight = False
        dc = 2
        USonicDist = 1000
        print "running..."

        if self._IRNbr == 2:
            while self._running:
                #read USonic sensor

                #if self._loopCount%2  == True:
                    #qualifier,dis = self._USonic.get_averageDistance()
                    #if qualifier == 1:
                        #USonicDist = dis
                    #else:
                        #print "wrong measurement"
                #self._loopCount += 1

                #read IR Sensor
                statusLeft  = self._IR.middle
                statusRight = self._IR.right

                if USonicDist > 10:
                    if statusLeft and statusRight:
                        self._MotorDrive.forward(dc)
                    elif statusLeft:
                        # line on the left => move left
                        self._MotorDrive.left(dc-1)
                    elif statusRight:
                        # line on the right => move right
                        self._MotorDrive.right(dc-1)
                else:
                    self._MotorDrive.stop(1)
                    print "Obstacle detected at "+ str(USonicDist)
        else:
            print "Nooo"

            """
            while self._running:
                if self._IR.getStatusLeft() == True:
                    statusLeft = 0b100
                else:
                    statusLeft = 0
                if self._IR.getStatusMiddle():
                    statusMiddle = 0b010
                else:
                    statusMiddle = 0
                if self._IR.getStatusRight():
                    statusRight  = 0b001
                else:
                    statusRight  = 0

                var = statusLeft+statusMiddle+statusRight
                """


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
        GPIO.cleanup()


