#!/usr/bin/python
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

"""Interface to Analog to Digital Converters."""

import time

import spidev


class AnalogToDigitalConverter():
    """Class to represent MCP3008 analog to digital Converter"""
    # Voltage dividers 1kOhm/1kOhm (channel 0-3) - 22kOhm/10kOhm(channel 4-7)
    _facCh0123 = 2
    _facCh4567 = 3.195
    # Bytes for building read commands
    start_byte = 0x01
    channel_modifier = 0x08
    end_byte = 0x00

    def __init__(self):
        self._spi = spidev.SpiDev()
        self._spi.open(0, 0)

    def _build_read_command(self, channel):
        """
        Produce 3-byte read command.

        The command is 1 byte, book-ended by start and end signifiers.
        """

        return [self.start_byte, (self.channel_modifier + channel) << 4,
                self.end_byte]

    def _process_adc_value(self, channel, value):
        """Return result of processing analog to digital converter value."""
        if channel < 4:
            coefficient = self._facCh0123
        else:
            coefficient = self._facCh4567
        return (((value[1] & 3) << 8) + value[2]) * 0.00322 * coefficient

    def read_adc(self, channel):
        """Read ADC channel."""
        if not 0 <= channel <= 7:
            raise ValueError("ADC number must be a value of 0-7!")
        r = self._spi.xfer2(self._build_read_command(channel))
        return self._process_adc_value(channel, r)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._spi.close()


if __name__ == '__main__':
    with AnalogToDigitalConverter() as mcp3008:
        while True:
            for ch in range(8):
                print("ADC Ch{0}[V]: {1}".format(ch, mcp3008.read_adc(ch)))
            print('-' * 80 + '\n')
            time.sleep(2)
