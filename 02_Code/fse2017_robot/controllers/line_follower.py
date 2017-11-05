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

from .. import Robot
from ..drivers.infrared import InfraredSensor
from ..drivers.led import LED


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
        self._robot = Robot()
        self._ir = InfraredSensor()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._running = False
        self._robot.__exit__()

    def run(self):
        state_left = False
        state_right = False

        while self._running:
            state_left = self._ir.middle
            state_right = self._ir.right
            distance = self._robot.obstacle
            if distance > 10:
                if state_left and state_right:
                    self._robot.drive(0.5)
                elif state_left:
                    # line on the left => move left
                    self._robot.turn(-10)
                elif state_right:
                    # line on the right => move right
                    self._robot.turn(10)
            else:
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
