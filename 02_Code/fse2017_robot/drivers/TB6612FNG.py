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

import sys
import time

import wiringpi
from gpio_manager import GPIO_Manager


class TB6612FNG(GPIO_Manager):
    """Interface with a TB6612FNG DC Motor driver."""
    _M1Dir1Pin = 6
    _M1Dir2Pin = 12
    _M1PWMPin_annex = 5  # solve error mapping (Vers.01)
    _M1PWMPin = 18
    _M2Dir1Pin = 19
    _M2Dir2Pin = 16
    _M2PWMPin_annex = 26  # solve error mapping (Vers.01)
    _M2PWMPin = 13
    _STBY = 20
    pins = [_M1Dir1Pin, _M1Dir2Pin, _M1PWMPin_annex, _M1PWMPin, _M2Dir1Pin,
            _M2Dir2Pin, _M2PWMPin_annex, _M2PWMPin, _STBY]

    def __init__(self):
        super(TB6612FNG, self).__init__()
        # Initialise inputs & outputs pins
        # Configure TB6612GNG Pins
        wiringpi.pinMode(self._M1Dir1Pin, wiringpi.OUTPUT)
        wiringpi.pinMode(self._M1Dir2Pin, wiringpi.OUTPUT)
        wiringpi.pinMode(self._M1PWMPin, wiringpi.PWM_OUTPUT)
        wiringpi.pinMode(self._M1PWMPin_annex, wiringpi.INPUT)
        wiringpi.pinMode(self._M2Dir1Pin, wiringpi.OUTPUT)
        wiringpi.pinMode(self._M2Dir2Pin, wiringpi.OUTPUT)
        wiringpi.pinMode(self._M2PWMPin, wiringpi.PWM_OUTPUT)
        wiringpi.pinMode(self._M2PWMPin_annex, wiringpi.INPUT)
        wiringpi.pinMode(self._STBY, wiringpi.OUTPUT)

    def to_dc(self, dc):
        return (1023 * dc) / 100

    def right_forward(self):
        wiringpi.digitalWrite(self._M1Dir1Pin, wiringpi.LOW)
        wiringpi.digitalWrite(self._M1Dir2Pin, wiringpi.HIGH)

    def right_back(self):
        wiringpi.digitalWrite(self._M1Dir1Pin, wiringpi.HIGH)
        wiringpi.digitalWrite(self._M1Dir2Pin, wiringpi.LOW)

    def left_back(self):
        wiringpi.digitalWrite(self._M2Dir1Pin, wiringpi.LOW)
        wiringpi.digitalWrite(self._M2Dir2Pin, wiringpi.HIGH)

    def left_forward(self):
        wiringpi.digitalWrite(self._M2Dir1Pin, wiringpi.HIGH)
        wiringpi.digitalWrite(self._M2Dir2Pin, wiringpi.LOW)

    def forward(self, duty_cycle=20):
        self.right_forward()
        self.left_forward()
        wiringpi.pwmWrite(self._M1PWMPin, self.to_dc(duty_cycle))
        wiringpi.pwmWrite(self._M2PWMPin, self.to_dc(duty_cycle))
        wiringpi.digitalWrite(self._STBY, wiringpi.HIGH)

    def reverse(self, duty_cycle=20):
        self.right_back()
        self.left_back()
        wiringpi.pwmWrite(self._M1PWMPin, self.to_dc(duty_cycle))
        wiringpi.pwmWrite(self._M2PWMPin, self.to_dc(duty_cycle))
        wiringpi.digitalWrite(self._STBY, wiringpi.HIGH)

    def right(self, duty_cycle=20):
        self.right_forward()
        self.left_back()
        wiringpi.pwmWrite(self._M1PWMPin, self.to_dc(duty_cycle))
        wiringpi.pwmWrite(self._M2PWMPin, self.to_dc(duty_cycle))
        wiringpi.digitalWrite(self._STBY, wiringpi.HIGH)

    def left(self, duty_cycle=20):
        self.right_back()
        self.left_forward()
        wiringpi.pwmWrite(self._M1PWMPin, self.to_dc(duty_cycle))
        wiringpi.pwmWrite(self._M2PWMPin, self.to_dc(duty_cycle))
        wiringpi.digitalWrite(self._STBY, wiringpi.HIGH)

    def stop(self):
        wiringpi.digitalWrite(self._M1Dir1Pin, wiringpi.LOW)
        wiringpi.digitalWrite(self._M1Dir2Pin, wiringpi.LOW)
        wiringpi.digitalWrite(self._M2Dir1Pin, wiringpi.LOW)
        wiringpi.digitalWrite(self._M2Dir2Pin, wiringpi.LOW)
        wiringpi.pwmWrite(self._M1PWMPin, 0)
        wiringpi.pwmWrite(self._M2PWMPin, 0)
        wiringpi.digitalWrite(self._STBY, wiringpi.LOW)

    def __exit__(self):
        wiringpi.pwmWrite(self._M1PWMPin, 0)
        wiringpi.pwmWrite(self._M2PWMPin, 0)
        super(TB6612FNG, self).__exit__()


if __name__ == '__main__':
    tb6612fng = TB6612FNG()
    try:
        while True:
            print "forward"
            tb6612fng.forward()
            time.sleep(3)

            tb6612fng.stop()
            time.sleep(3)

            print "reverse"
            tb6612fng.reverse()
            time.sleep(3)

            tb6612fng.stop()
            time.sleep(3)

            print "left"
            tb6612fng.left()
            time.sleep(3)

            tb6612fng.stop()
            time.sleep(3)

            print "right"
            tb6612fng.right()
            time.sleep(3)

            tb6612fng.stop()
            time.sleep(3)
            print "Done!"

    except KeyboardInterrupt:
        tb6612fng.__exit__()
        sys.exit(0)
