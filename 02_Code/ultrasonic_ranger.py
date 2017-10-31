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

import wiringpi

GPIO_OUT = 1
GPIO_IN = 0
INPUT_MODE = 0


class UltrasonicTimeoutError(Exception):
    """UltrasonicRanger does not measure response to ping."""


class UltrasonicRanger(object):
    """Interface with an HCSR04 ultrasonic range sensor."""

    _trigger_pin = 15
    _echo_pin = 14
    _timeout = 0.1  # seconds
    _average_count = 1

    def __init__(self):
        # TODO: Setup should be made once, not multiple times
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(self._trigger_pin, GPIO_OUT)
        wiringpi.pinMode(self._echo_pin, GPIO_IN)

    def get_distance(self):
        """Measure time between sent impulse and measured reflectance."""

        def sense_echo_pin_change(initial_state, timeout):
            """Return time at which the echo pin's state changed."""
            while wiringpi.digitalRead(self._echo_pin) == initial_state:
                if time.time() > timeout:
                    raise UltrasonicTimeoutError("No response measured before "
                                                 "timeout.")
            return time.time()

        wiringpi.digitalWrite(self._trigger_pin, 0)
        time.sleep(0.000002)
        wiringpi.digitalWrite(self._trigger_pin, 1)
        time.sleep(0.00001)
        wiringpi.digitalWrite(self._trigger_pin, 0)

        timeout_end = time.time() + self._timeout

        time1 = sense_echo_pin_change(0, timeout_end)
        time2 = sense_echo_pin_change(1, timeout_end)

        duration = time2 - time1
        distance = duration * 340.0 / 2.0 * 100
        return distance

    def get_average_distance(self):
        """Average multiple distance measurements."""
        distance_sum = 0.0
        error_count = 0
        for i in range(self._average_count):
            try:
                distance = self.get_distance()
                distance_sum += distance
            except UltrasonicTimeoutError:
                error_count += 1
            if error_count > min(3, self._average_count) or distance_sum == 0:
                raise UltrasonicTimeoutError("3 consecutive bad soundings.")
        return distance_sum / self._average_count

    def __enter__(self):
        return self

    def __exit__(self, *args):
        for pin in self._trigger_pin, self._echo_pin:
            wiringpi.digitalWrite(pin, 0)
            wiringpi.pinMode(pin, INPUT_MODE)


if __name__ == "__main__":
    with UltrasonicRanger() as ultrasonic:
        while True:
            try:
                dis = ultrasonic.get_average_distance()
                print(dis)
            except UltrasonicTimeoutError:
                print("Error during reading.")
            time.sleep(1)
