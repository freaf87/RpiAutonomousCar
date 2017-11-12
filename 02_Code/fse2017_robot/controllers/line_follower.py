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

from fse2017_robot import Robot
from fse2017_robot.drivers.led import LED


class HeartBeat(object):
    """Heartbeat thread."""

    def __init__(self):
        self._running = False
        self._LED = LED()

    def run(self):
        self._running = True
        while self._running:
            self._LED.toggle()
            time.sleep(0.5)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._running = False
        self._LED.__exit__()


class LineFollower:
    def __init__(self):
        self._running = True
        self._robot = Robot()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._running = False
        self._robot.__exit__()

    def run(self):
        while self._running:
            state_left = self._robot.infrared.middle
            state_right = self._robot.infrared.right
            distance = self._robot.obstacle
            if distance > 10:
                if state_left and state_right:
                    self._robot.drive(0.5)
                elif state_left:
                    # line on the left => move left
                    self._robot.motor.left()
                elif state_right:
                    # line on the right => move right
                    self._robot.motor.right()
                else:
                    self._robot.motor.right()
            else:
                print("Obstacle detected at " + str(distance))
            distance = self._robot.obstacle


if __name__ == "__main__":
    with HeartBeat() as heartbeat, LineFollower() as line_follower:
        # Spawn threads
        heartbeat = HeartBeat()
        heartbeat_thread = Thread(target=heartbeat.run)
        heartbeat_thread.start()

        line_follower = LineFollower()
        line_follower_thread = Thread(target=line_follower.run)
        line_follower_thread.start()

        # Keep running
        try:
            while True:
                time.sleep(0.5)
        except KeyboardInterrupt:
            heartbeat._running = False
            line_follower._running = False

