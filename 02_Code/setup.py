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

from distutils.core import setup

setup(
    name='fse2017_robot',
    version='v0.1.0',
    requires=['spidev', 'wiringpi'],
    packages=['fse2017_robot',
              'fse2017_robot.drivers',
              'fse2017_robot.controllers'],
    url='https://fullstackembedded.com',
    license='GNU GPL',
    author='Daniel Lee',
    author_email='erget2005@gmail.com',
    description="Drivers and various driving aids for FSE 2017\'s Raspberry "
                "Pi-based robot.",
    long_description=open('README').read()
)
