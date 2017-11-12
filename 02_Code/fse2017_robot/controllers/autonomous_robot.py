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

"""Demonstrate basic autonomous driving."""

import sys

from fse2017_robot import Robot

if __name__ == "__main__":
    try:
        with Robot() as r:
            while True:
                distance = r.obstacle
                if distance > 20:
                    r.set_drive_mode(1)
                else:
                    r.turn(90 - distance)
    except KeyboardInterrupt:
        sys.exit(0)
