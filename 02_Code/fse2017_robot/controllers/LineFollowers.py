#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of FSE 2017.
#
# FSE 2017 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FSE 2017 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with FSE 2017.  If not, see <http://www.gnu.org/licenses/>.

"""Line following demonstration."""

import time
from threading import Thread

import RPi.GPIO as GPIO
from ..drivers.ultrasonic_ranger import UltrasonicRanger

from ..drivers.TB6612FNG import TB6612FNG
from ..drivers.infrared import InfraredSensor
from ..drivers.led import LED


class HeartBeat(object):
    """Heartbeat thread."""

    def __init__(self):
        self._running = False
        self._LED = LED()

    def terminate(self):
        self._running = False

    def run(self):
        self._running = True
        while self._running:
            self._LED.on()
            time.sleep(0.5)
            self._LED.off()
            time.sleep(0.5)


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
        statusLeft = False
        statusRight = False
        dc = 2
        USonicDist = 1000
        print "running..."

        if self._IRNbr == 2:
            while self._running:
                # read USonic sensor

                # if self._loopCount%2  == True:
                # qualifier,dis = self._USonic.get_averageDistance()
                # if qualifier == 1:
                # USonicDist = dis
                # else:
                # print "wrong measurement"
                # self._loopCount += 1

                # read IR Sensor
                statusLeft = self._IR.middle
                statusRight = self._IR.right

                if USonicDist > 10:
                    if statusLeft and statusRight:
                        self._MotorDrive.forward(dc)
                    elif statusLeft:
                        # line on the left => move left
                        self._MotorDrive.left(dc - 1)
                    elif statusRight:
                        # line on the right => move right
                        self._MotorDrive.right(dc - 1)
                else:
                    self._MotorDrive.stop(1)
                    print "Obstacle detected at " + str(USonicDist)
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
        HeartBeatThread = Thread(target=Th1.run)
        HeartBeatThread.start()

        Th2 = LineFollower()
        RpiAutCarThread = Thread(target=Th2.run)
        RpiAutCarThread.start()

        while True:
            pass
    except KeyboardInterrupt:
        Th1.terminate()
        Th2.terminate()
        GPIO.cleanup()
