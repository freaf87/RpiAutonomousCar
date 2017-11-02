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

"""Driver for a GPIO LED."""

import time

import wiringpi

from gpio_manager import GPIO_Manager


class LED(GPIO_Manager):
    """Driver for an LED connected by GPIO."""

    _pin = 21
    _pins = [_pin]

    def __init__(self):
        super(LED, self).__init__()
        wiringpi.pinMode(self._pin, self.GPIO_OUT)
        self.state = False

    def on(self):
        wiringpi.digitalWrite(self._pin, self.GPIO_OUT)
        self.state = True

    def off(self):
        wiringpi.digitalWrite(self._pin, self.GPIO_IN)
        self.state = False

    def toggle(self):
        if self.state:
            self.off()
        else:
            self.on()


if __name__ == "__main__":
    with LED() as led:
        while 1:
            led.on()
            time.sleep(0.5)
            led.off()
            time.sleep(0.5)
