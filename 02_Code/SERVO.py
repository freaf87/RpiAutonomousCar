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

import time
import RPi.GPIO as GPIO


# TODO: Is this used anywhere? Otherwise let's remove it.
# TODO: Rename, all caps looks like constant & immutable. Plus docstrings.
class SERVO():
    def __init__(self):
        # TODO: PEP8, plus make this class attribute.
        self._ServoPin = 4
        # TODO: Long-term we should think about if we set the GPIO mode in
        # each hardware class - it's a lot of setting on initialization and
        # would probably be more efficient to have some kind of managing
        # class that takes care of all these things for us and gives us the
        # sensors, servos, etc. via a factory. Not important now though.
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._ServoPin, GPIO.OUT)
        # TODO: PEP8
        self._ServoPWM = GPIO.PWM(self._ServoPin,50)
        self._ServoPWM.start(7.5)


    def loop(self):
        while True:
            self._ServoPWM.ChangeDutyCycle(7.5)
            time.sleep(1)
            self._ServoPWM.ChangeDutyCycle(12.5)
            time.sleep(1)
            self._ServoPWM.ChangeDutyCycle(2.5)
            time.sleep(1)

    def destroy(self):
        self._ServoPWM.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    servo = SERVO()
    try:
        servo.loop()
    except KeyboardInterrupt:
        servo.destroy()

