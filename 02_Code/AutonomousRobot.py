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
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

import time

from LED import LED
from MotorDriver import MotorDriver
from UltrasonicRanger import UltrasonicRanger


def loop(sensor, drive):
    duty_cycle = 4

    while True:
        # TODO: Replace with try-except clause, e.g.
        # try:
        #      distance = sensor.get_average_distance()
        # except BadDistanceException:
        #      pass
        qualifier, distance = sensor.get_average_distance()
        if qualifier == 1:
            if distance < 20:
                drive.stop()
                time.sleep(0.01)
                drive.reverse(duty_cycle - 2)
                time.sleep(0.25)
                drive.left(duty_cycle - 2)
                time.sleep(0.25)
                drive.forward(duty_cycle)
            else:
                drive.forward()

        else:
            pass


if __name__ == "__main__":
    try:
        ultrasonic = UltrasonicRanger()
        led = LED()
        robot_drive = MotorDriver()
        loop(ultrasonic, robot_drive)
    except KeyboardInterrupt:
        ultrasonic.destroy()
