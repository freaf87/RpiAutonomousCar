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
import math
import wiringpi
from smbus import SMBus
from gpio_manager import GPIO_Manager

# Registers/etc:
PCA9685_ADDRESS    = 0x54
MODE1              = 0x00
MODE2              = 0x01
SUBADR1            = 0x02
SUBADR2            = 0x03
SUBADR3            = 0x04
PRESCALE           = 0xFE
LED0_ON_L          = 0x06
LED0_ON_H          = 0x07
LED0_OFF_L         = 0x08
LED0_OFF_H         = 0x09
ALL_LED_ON_L       = 0xFA
ALL_LED_ON_H       = 0xFB
ALL_LED_OFF_L      = 0xFC
ALL_LED_OFF_H      = 0xFD

# Bits:
RESTART            = 0x80
SLEEP              = 0x10
ALLCALL            = 0x01
INVRT              = 0x10
OUTDRV             = 0x04

class DriverError(Exception):
    """ Error occurs when communicating with driver """

class i2cError(DriverError):
    """ Raised when i2c error occurs """

class PCA9685(GPIO_Manager):
    """Driver for PCA9685 PWM/LED Servo controller connected via I2C"""
    
    def __init__(self, address= PCA9685_ADDRESS):
        super(PCA9685, self).__init__()

        # Setup I2C interface for the device
        self._i2cbus = SMBus(1) # deviceNbr = 1 for newer Rpis (adapt for older revision)
        self._i2cbus.write_byte_data(PCA9685_ADDRESS, MODE2, OUTDRV)
        self._i2cbus.write_byte_data(PCA9685_ADDRESS, MODE1, ALLCALL)
        time.sleep(0.005)  # wait for oscillator
        mode1 = self._i2cbus.read_byte_data(PCA9685_ADDRESS, MODE1)
        mode1 = mode1 & ~SLEEP  # wake up (reset sleep)
        self._i2cbus.write_byte_data(PCA9685_ADDRESS, MODE1, mode1)
        time.sleep(0.005)  # wait for oscillator

    def set_pwm_freq(self, freq_hz):
        """Set the PWM frequency to the provided value in hertz."""
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq_hz)
        prescaleval -= 1.0
        prescale = int(math.floor(prescaleval + 0.5))
        oldmode = self._i2cbus.read_byte_data(PCA9685_ADDRESS, MODE1);
        newmode = (oldmode & 0x7F) | 0x10    # sleep
        self._i2cbus.write_byte_data(PCA9685_ADDRESS, MODE1, newmode)  # go to sleep
        self._i2cbus.write_byte_data(PCA9685_ADDRESS, PRESCALE, prescale)
        self._i2cbus.write_byte_data(PCA9685_ADDRESS, MODE1, oldmode)
        time.sleep(0.005)
        self._i2cbus.write_byte_data(PCA9685_ADDRESS, MODE1, oldmode | 0x80)

    def set_pwm(self, channel, on, off):
        """Sets a single PWM channel."""
        self._i2cbus.write_byte_data(PCA9685_ADDRESS, LED0_ON_L+4*channel, on & 0xFF)
        self._i2cbus.write_byte_data(PCA9685_ADDRESS, LED0_ON_H+4*channel, on >> 8)
        self._i2cbus.write_byte_data(PCA9685_ADDRESS, LED0_OFF_L+4*channel, off & 0xFF)
        self._i2cbus.write_byte_data(PCA9685_ADDRESS, LED0_OFF_H+4*channel, off >> 8)

    def set_all_pwm(self, on, off):
        """Sets all PWM channels."""
        self._i2cbus.write_byte_data(PCA9685_ADDRESS, ALL_LED_ON_L, on & 0xFF)
        self._i2cbus.write_byte_data(PCA9685_ADDRESS, ALL_LED_ON_H, on >> 8)
        self._i2cbus.write_byte_data(PCA9685_ADDRESS, ALL_LED_OFF_L, off & 0xFF)
        self._i2cbus.write_byte_data(PCA9685_ADDRESS, ALL_LED_OFF_H, off >> 8)



if __name__ == "__main__":
    with PCA9685() as pwm_driver:
        # Configure min and max servo pulse lengths
        servo_min = 150  # Min pulse length out of 4096
        servo_max = 600  # Max pulse length out of 4096
        pwm_driver.set_pwm_freq(60)

        while 1:
            pwm_driver.set_pwm(9, 0, servo_min)
            time.sleep(1)
            pwm_driver.set_pwm(9, 0, servo_max)
            time.sleep(1)

        
