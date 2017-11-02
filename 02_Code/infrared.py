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

"""Driver for GPIO infrared device."""

import time

import wiringpi

from gpio_manager import GPIO_Manager


class InfraredSensor(GPIO_Manager):
    """A trisensor infrared ranger."""

    _left = 27
    _middle = 18
    _right = 17
    _pins = [_left, _middle, _right]

    def __init__(self):
        super(InfraredSensor, self).__init__()
        for pin in self._pins:
            wiringpi.pinMode(pin, self.GPIO_IN)

    @property
    def left(self):
        """Obstacle sensed on left sensor?"""
        return wiringpi.digitalRead(self._left)

    @property
    def middle(self):
        """Obstacle sensed on middle sensor?"""
        return wiringpi.digitalRead(self._middle)

    @property
    def right(self):
        """Obstacle sensed on right sensor?"""
        return wiringpi.digitalRead(self._right)


if __name__ == "__main__":
    with InfraredSensor() as infrared:
        while True:
            statusLeft = infrared.left
            statusMiddle = infrared.middle
            statusRight = infrared.right
            print("statusLeft   = {0}".format(str(statusLeft)))
            print("statusMiddle = {0}".format(str(statusMiddle)))
            print("statusRight  = {0}".format(str(statusRight)))
            time.sleep(1)
