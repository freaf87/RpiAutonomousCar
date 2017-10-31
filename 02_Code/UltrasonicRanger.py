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


class UltrasonicRanger():

    """Interface with an HCSR04 ultrasonic range sensor."""

    def __init__(self):
        # TODO: These are static, make these class attributes
        self._trigger_pin = 15
        self._echo_pin = 14
        self._timeout  = 0.10 #[s]
        self._average_count = 1

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._trigger_pin, GPIO.OUT)
        GPIO.setup(self._echo_pin, GPIO.IN)

    def get_distance(self):
        #send impulse
        GPIO.output(self._trigger_pin, 0)
        time.sleep(0.000002)

        GPIO.output(self._trigger_pin, 1)
        time.sleep(0.00001)
        GPIO.output(self._trigger_pin, 0)

        #timeout
        timeout_end = time.time()+ self._timeout

        #wait for response
        while GPIO.input(self._echo_pin) == 0:
            if time.time() > timeout_end:
                return -1, -1
        time1 = time.time()
        while GPIO.input(self._echo_pin) == 1:
            if time.time() > timeout_end:
                return -1, -1
        time2 = time.time()

        #calculate the distance
        during = time2 - time1
        # TODO: Don't return a tuple, return the value. First item not needed
        #  as if function is non-nominal an error is raised.
        return 1, during * 340.0 / 2.0 * 100

    def get_average_distance(self):
        i = 0
        distance = 0
        # TODO: PEP8
        errorCount = 0
        while i < self._average_count:
            qualifier, tmp = self.get_distance()
            if qualifier != -1:
                # TODO: Replace these with += operator
                i = i + 1
                distance = distance + tmp
            else:
                errorCount = errorCount
            if errorCount > 3:
                return -1, -1
        # TODO: No tuple, return actual value
        # TODO: Cast to float, don't multiply by 1.0
        return 1, distance/(self._average_count * 1.0)

    def destroy(self):
        GPIO.cleanup()


if __name__ == "__main__":
    ultrasonic = UltrasonicRanger()
    try:
        while True:
            qualifier,dis = ultrasonic.get_average_distance()
            if qualifier == 1:
                print dis, 'cm'
            else:
                print "Error during reading"

            time.sleep(1)

    except KeyboardInterrupt:
        ultrasonic.destroy()
