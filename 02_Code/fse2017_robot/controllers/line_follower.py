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

from ..drivers.TB6612FNG import TB6612FNG
from ..drivers.infrared import InfraredSensor
from ..drivers.led import LED
from ..drivers.ultrasonic_ranger import UltrasonicRanger


class HeartBeat(object):
    """Heartbeat thread."""

    def __init__(self):
        self._running = False
        self._LED = LED()

    def __exit(self, *args):
        self._running = False

    def run(self):
        self._running = True
        while self._running:
            self._LED.toggle()
            time.sleep(0.5)


class LineFollower:
    def __init__(self):
        self._running = True
        self._ir = InfraredSensor()
        self._motordrive = TB6612FNG()
        self._ultrasonic = UltrasonicRanger()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._running = False
        for x in self._ir, self._motordrive, self._ultrasonic:
            x.__exit__()

    def run(self):
        state_left = False
        state_right = False
        dc = 2

        while self._running:

            # read IR Sensor
            state_left = self._ir.middle
            state_right = self._ir.right

            distance = self._ultrasonic.obstacle
            if distance > 10:
                if state_left and state_right:
                    self._motordrive.forward(dc)
                elif state_left:
                    # line on the left => move left
                    self._motordrive.left(dc - 1)
                elif state_right:
                    # line on the right => move right
                    self._motordrive.right(dc - 1)
            else:
                self._motordrive.stop(1)
                print("Obstacle detected at " + str(distance))
            distance = self._ultrasonic


if __name__ == "__main__":
    try:
        # Spawn threads
        heartbeat = HeartBeat()
        heartbeat_thread = Thread(target=heartbeat.run)
        heartbeat_thread.start()

        line_follower = LineFollower()
        line_follower_thread = Thread(target=line_follower.run)
        line_follower_thread.start()

        # Keep running
        while True:
            pass

    except KeyboardInterrupt:
        heartbeat.__exit__()
        line_follower.__exit__()
