#!/usr/bin/python
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

"""Driver for motor drivers."""

import sys
import time

import wiringpi
from gpio_manager import GPIO_Manager


# TODO: DRY this code (WET)
# TODO: This class cleans up after itself, so it should be used as a context
# manager like this:
# with MotorDriver() as m:
#     m.do_stuff()
# ...
# When an exception occurs or the with-block is completed, the object cleans
# up after itself automatically.

# TODO: Maybe break this down into the component motors with forward and back
#  methods
class MotorDriver(GPIO_Manager):
    """Interface with a TB6612FNG DC Motor driver."""

    _M1Dir1Pin = 6
    _M1Dir2Pin = 12
    _M1PWMPin = 5
    _M2Dir1Pin = 19
    _M2Dir2Pin = 16
    _M2PWMPin = 26
    _STBYPin = 13
    pins = [_M1Dir1Pin, _M1Dir2Pin, _M1PWMPin, _M2Dir1Pin, _M2Dir2Pin,
            _M2PWMPin, _STBYPin]

    def __init__(self):
        for pin in self.pins:
            wiringpi.pinMode(pin, wiringpi.OUTPUT)
        wiringpi.softPwmCreate(self._M1PWMPin, 0, 100)
        wiringpi.softPwmCreate(self._M2PWMPin, 0, 100)

    # TODO: Each direction sets 4 GPIOs, we can store these in the class, e.g.
    # >>> md = MotorDriver()
    # >>> md.drive(md.directions.left)
    # And then this would call internally something like:
    # (inside MotorDriver):
    # ...
    #     def drive(direction, duty_cycle):
    #         for pin, val in direction:
    #             GPIO.output(pin, val)
    # Here the directions would be on the class, stored as a tuple of tuples,
    #  where each inner tuple would store the pin and the value it should be
    # set to.

    def forward(self, duty_cycle=20):
        wiringpi.digitalWrite(self._M1Dir1Pin, wiringpi.INPUT)
        wiringpi.digitalWrite(self._M1Dir2Pin, wiringpi.OUTPUT)
        wiringpi.softPwmWrite(self._M1PWMPin, duty_cycle)

        wiringpi.digitalWrite(self._M2Dir1Pin, wiringpi.OUTPUT)
        wiringpi.digitalWrite(self._M2Dir2Pin, wiringpi.INPUT)
        wiringpi.softPwmWrite(self._M2PWMPin, duty_cycle)

        wiringpi.digitalWrite(self._STBYPin, wiringpi.OUTPUT)

    def reverse(self, duty_cycle=20):
        wiringpi.digitalWrite(self._M1Dir1Pin, wiringpi.OUTPUT)
        wiringpi.digitalWrite(self._M1Dir2Pin, wiringpi.INPUT)
        wiringpi.softPwmWrite(self._M1Pwm, duty_cycle)

        wiringpi.digitalWrite(self._M2Dir1Pin, wiringpi.INPUT)
        wiringpi.digitalWrite(self._M2Dir2Pin, wiringpi.OUTPUT)
        wiringpi.softPwmWrite(self._M2Pwm, duty_cycle)

        wiringpi.digitalWrite(self._STBYPin, wiringpi.OUTPUT)

    def left(self, duty_cycle=8):
        wiringpi.digitalWrite(self._M1Dir1Pin, wiringpi.OUTPUT)
        wiringpi.digitalWrite(self._M1Dir2Pin, wiringpi.INPUT)
        wiringpi.softPwmWrite(self._M1Pwm, duty_cycle)

        wiringpi.digitalWrite(self._M2Dir1Pin, wiringpi.OUTPUT)
        wiringpi.digitalWrite(self._M2Dir2Pin, wiringpi.INPUT)
        wiringpi.softPwmWrite(self._M2Pwm, duty_cycle)

        wiringpi.digitalWrite(self._STBYPin, wiringpi.OUTPUT)

    def right(self, duty_cycle=8):
        wiringpi.digitalWrite(self._M1Dir1Pin, wiringpi.INPUT)
        wiringpi.digitalWrite(self._M1Dir2Pin, wiringpi.OUTPUT)
        wiringpi.softPwmWrite(self._M1Pwm, duty_cycle)

        wiringpi.digitalWrite(self._M2Dir1Pin, wiringpi.INPUT)
        wiringpi.digitalWrite(self._M2Dir2Pin, wiringpi.OUTPUT)
        wiringpi.softPwmWrite(self._M2Pwm, duty_cycle)

        wiringpi.digitalWrite(self._STBYPin, wiringpi.OUTPUT)

    def stop(self):
        wiringpi.digitalWrite(self._M1Dir1Pin, wiringpi.INPUT)
        wiringpi.digitalWrite(self._M1Dir2Pin, wiringpi.INPUT)
        # self._M1Pwm.stop()
        wiringpi.softPwmWrite(self._M1Pwm, wiringpi.INPUT)

        wiringpi.digitalWrite(self._M2Dir1Pin, wiringpi.INPUT)
        wiringpi.digitalWrite(self._M2Dir2Pin, wiringpi.INPUT)
        # self._M2Pwm.stop()
        wiringpi.softPwmWrite(self._M2Pwm, wiringpi.INPUT)

        wiringpi.digitalWrite(self._STBYPin, wiringpi.INPUT)


if __name__ == '__main__':
    tb6612fng = MotorDriver()
    try:
        print "forward"
        time.sleep(3)
        tb6612fng.forward()

        tb6612fng.stop()
        time.sleep(3)

        print "reverse"
        time.sleep(3)
        tb6612fng.reverse()

        tb6612fng.stop()
        time.sleep(3)

        print "left"
        time.sleep(3)
        tb6612fng.left()

        tb6612fng.stop()
        time.sleep(3)

        print "right"
        time.sleep(3)
        tb6612fng.right()

        tb6612fng.stop()
        time.sleep(3)
        print "Done!"

    except KeyboardInterrupt:
        tb6612fng.__exit__()
