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


class UltrasonicTimeoutError(Exception):
    """UltrasonicRanger does not measure response to ping."""


class UltrasonicRanger():
    """Interface with an HCSR04 ultrasonic range sensor."""

    _trigger_pin = 15
    _echo_pin = 14
    _timeout = 0.1  # seconds
    _average_count = 1

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._trigger_pin, GPIO.OUT)
        GPIO.setup(self._echo_pin, GPIO.IN)

    def get_distance(self):
        """Measure time between sent impulse and measured reflectance."""

        def sense_echo_pin_change(initial_state, timeout_end):
            """Return time at which the echo pin's state changed."""
            while GPIO.input(self._echo_pin) == initial_state:
                if time.time() > timeout_end:
                    raise UltrasonicTimeoutError("No response measured before "
                                                 "timeout.")
            return time.time()

        GPIO.output(self._trigger_pin, 0)
        time.sleep(0.000002)
        GPIO.output(self._trigger_pin, 1)
        time.sleep(0.00001)
        GPIO.output(self._trigger_pin, 0)

        timeout_end = time.time() + self._timeout

        time1 = sense_echo_pin_change(0, timeout_end)
        time2 = sense_echo_pin_change(1, timeout_end)

        duration = time2 - time1
        return duration * 340.0 / 2.0 * 100

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
            if error_count > 3:
                raise UltrasonicTimeoutError("3 consecutive bad soundings.")
        return distance_sum / self._average_count

    def __enter__(self):
        return self

    def __exit__(self, *args):
        GPIO.cleanup()


if __name__ == "__main__":
    with UltrasonicRanger() as ultrasonic:
        while True:
            try:
                dis = ultrasonic.get_average_distance()
                print(dis)
            except UltrasonicTimeoutError:
                print("Error during reading.")
            time.sleep(1)
