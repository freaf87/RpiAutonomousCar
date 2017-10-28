#!/usr/bin/env python

import time

from LED import LED
from MotorDriver import MotorDriver
from UltrasonicRanger import UltrasonicRanger


class Robot(object):

    """The robot used for FSE 2017."""

    def __init__(self):
        self.ultrasonic = UltrasonicRanger()
        self.led = LED()
        self.motor = MotorDriver()
        self.duty_cycle = 4

    def drive(self, distance):
        """
        Drive a given distance.

        distance is signed - positive for forwards, negative for backwards.
        """
        if distance > 0:
            self.motor.forward(self.duty_cycle)
        elif distance < 0:
            self.motor.reverse(self.duty_cycle)
        time.sleep(abs(distance))
        self.motor.stop()

    def destroy(self):
        """Release internally used resources."""
        self.ultrasonic.destroy()
