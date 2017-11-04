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
import sys
import wiringpi as gpio

class TB6612FNG():
    """
    Class to represent TB6612FNG DC Motor driver
    """

    def __init__(self):
        # Initialise inputs & outputs pins
        # TODO: These are shared across all objects, so make them class
        # attributes rather than setting them on initialization
        self._M1Dir1Pin = 6
        self._M1Dir2Pin = 12
        self._M1PWMPin_annex  = 5  #solve error mapping (Vers.01)
        self._M1PWMPin  = 18
        self._M2Dir1Pin = 19
        self._M2Dir2Pin = 16
        self._M2PWMPin_annex  = 26 #solve error mapping (Vers.01)
        self._M2PWMPin = 13
        self._STBY =  20

        # Configure TB6612GNG Pins
        gpio.wiringPiSetupGpio ()
        gpio.pinMode(self._M1Dir1Pin,1)
        gpio.pinMode(self._M1Dir2Pin,1)
        gpio.pinMode(self._M1PWMPin,2)
        gpio.pinMode(self._M1PWMPin_annex, 0)
        gpio.pinMode(self._M2Dir1Pin,1)
        gpio.pinMode(self._M2Dir2Pin,1)
        gpio.pinMode(self._M2PWMPin,2)
        gpio.pinMode(self._M2PWMPin_annex, 0)
        gpio.pinMode(self._STBY, 1)

    def getDC(self, dc):
        return (1023*dc)/100

    def M1CounterClkwise(self):
        gpio.digitalWrite(self._M1Dir1Pin, 0)
        gpio.digitalWrite(self._M1Dir2Pin, 1)

    def M1Clkwise(self):
        gpio.digitalWrite(self._M1Dir1Pin, 1)
        gpio.digitalWrite(self._M1Dir2Pin, 0)

    def M2CounterClkwise(self):
        gpio.digitalWrite(self._M2Dir1Pin, 0)
        gpio.digitalWrite(self._M2Dir2Pin, 1)

    def M2Clkwise(self):
        gpio.digitalWrite(self._M2Dir1Pin, 1)
        gpio.digitalWrite(self._M2Dir2Pin, 0)

    def forward(self, dutyCycle = 20):
        self.M1CounterClkwise()
        self.M2Clkwise()
        gpio.pwmWrite(self._M1PWMPin, self.getDC(dutyCycle))
        gpio.pwmWrite(self._M2PWMPin, self.getDC(dutyCycle))
        gpio.digitalWrite(self._STBY, 1)

    def reverse(self, dutyCycle = 20):
        self.M1Clkwise()
        self.M2CounterClkwise()
        gpio.pwmWrite(self._M1PWMPin, self.getDC(dutyCycle))
        gpio.pwmWrite(self._M2PWMPin, self.getDC(dutyCycle))
        gpio.digitalWrite(self._STBY, 1)

    def right(self, dutyCycle = 20):
        self.M1CounterClkwise()
        self.M2CounterClkwise()
        gpio.pwmWrite(self._M1PWMPin, self.getDC(dutyCycle))
        gpio.pwmWrite(self._M2PWMPin, self.getDC(dutyCycle))
        gpio.digitalWrite(self._STBY, 1)

    def left(self, dutyCycle = 20):
        self.M1Clkwise()
        self.M2Clkwise()
        gpio.pwmWrite(self._M1PWMPin, self.getDC(dutyCycle))
        gpio.pwmWrite(self._M2PWMPin, self.getDC(dutyCycle))
        gpio.digitalWrite(self._STBY, 1)

    def stop(self):
        gpio.digitalWrite(self._M1Dir1Pin, 0)
        gpio.digitalWrite(self._M1Dir2Pin, 0)
        gpio.digitalWrite(self._M2Dir1Pin, 0)
        gpio.digitalWrite(self._M2Dir2Pin, 0)
        gpio.pwmWrite(self._M1PWMPin, 0)
        gpio.pwmWrite(self._M2PWMPin, 0)
        gpio.digitalWrite(self._STBY, 0)

    # TODO: Rename to __exit__ so that this is called on exceptions or when
    # exiting context
    def destroy(self):
        gpio.pwmWrite(self._M1PWMPin , 0)
        gpio.pinMode (self._M1PWMPin , 0)
        gpio.pwmWrite(self._M2PWMPin , 0)
        gpio.pinMode (self._M2PWMPin , 0)
        gpio.pinMode (self._M1Dir1Pin, 0)
        gpio.pinMode (self._M1Dir2Pin, 0)
        gpio.pinMode (self._M2Dir1Pin, 0)
        gpio.pinMode (self._M2Dir2Pin, 0)


if __name__ == '__main__':
    tb6612fng = MotorDriver()
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
        tb6612fng.destroy()
        sys.exit(0)
