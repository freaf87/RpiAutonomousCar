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

"""Tests for all movement functions of the FSE 2017 robot's public API."""

from time import sleep

from robot import Robot


class TestRobotMovement(object):
    """Interactive tests for robot motion."""

    def setup(self):
        self.r = Robot(10)

    def teardown(self):
        self.r.__exit__()

    def test_back_and_forth(self):
        """Test y-axis motion."""
        raw_input("DRIVE TEST: Clear path in front of and behind robot "
                  "for 5 cm and press Enter.")
        motions = [1, -2, 1]
        for motion in motions:
            self.r.drive(motion)
        report = raw_input("Did robot move as follows? {} \n"
                           "(Y/n): ".format(motions))
        assert (not report or report.lower() == 'y')

    def test_turning(self):
        """Test turning."""
        raw_input("TURN TEST: Press Enter when robot rotation is ready.")
        self.r.turn(45)
        self.r.turn(-450)
        self.r.turn(405)
        report = raw_input("Did robot turn 45° clockwise, then 450° "
                           "counterclockwise, then back to start? \n"
                           "(Y/n): ")
        assert (not report or report.lower() == 'y')

    def test_drive_arc(self):
        """Drive in arcs."""
        raw_input("ARC TEST: Clear ground 15cm to right and front and "
                  "press Enter.")
        self.r.drive_curve(2, 90)
        self.r.drive_curve(2, -90)
        self.r.turn(-135)
        self.r.drive(3.6)
        self.r.turn(135)
        report = raw_input("Did robot drive an arc to right, "
                           "then to left, then return to start? \n"
                           "(Y/n): ")
        assert (not report or report.lower() == 'y')

    def test_obstacle_detection(self):
        """Report obstacles correctly."""
        raw_input("ULTRASONIC TEST: Place obstacle within 20 cm of robot "
                  "and press Enter.")
        assert (self.r.obstacle < 20)
        raw_input("Clear ground before robot and press enter.")
        assert (self.r.obstacle > 20)

    def test_led(self):
        """Blink LED on and off."""
        raw_input("LED TEST: LED will blink on and off twice.")
        self.r.led.on()
        sleep(0.5)
        self.r.led.off()
        sleep(0.5)
        self.r.led.toggle()
        sleep(0.5)
        self.r.led.toggle()
        report = raw_input("Did LED blink on and off twice, once every half "
                           "second? (Y/n): ")
        assert (not report or report.lower() == 'y')


if __name__ == "__main__":
    suite = TestRobotMovement()
    try:
        suite.setup()
        tests = [fun for fun in dir(suite) if
                 callable(getattr(suite, fun)) and
                 fun.startswith("test")]
        for test in tests:
            try:
                getattr(suite, test)()
            except KeyboardInterrupt:
                print("\nSkipping test.")
    finally:
        suite.teardown()
