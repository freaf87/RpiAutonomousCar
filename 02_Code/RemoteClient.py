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

import pygame
from threading import Thread
from logging import debug
import socket, time, sys

IP_ADDRESS = "192.168.0.31"
IP_PORT = 22000

KEY_TEXT = {
    pygame.K_UP: "forward",
    pygame.K_DOWN: "reverse",
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right"
}

class Receiver(Thread):
    BUFFER_SIZE = 4096
    END_OF_MESSAGE_INDICATOR = "\0"

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        debug("Connecting...")
        try:
            self.sock.connect((IP_ADDRESS, IP_PORT))
        except socket.gaierror as error:
            debug("Connection failed.")
            raise RuntimeError(
                "Connection to {}:{:d} failed".format(IP_ADDRESS, IP_PORT))

    def close_connection(self):
        debug("Closing socket")
        self.sock.close()

    def send_command(self, cmd):
        debug("sendCommand() with cmd = " + cmd)
        try:
            self.sock.sendall(cmd + self.END_OF_MESSAGE_INDICATOR)
        except socket.error:
            debug("Exception in sendCommand()")
            self.close_connection()


if __name__ == "__main__":
    try:
        pygame.init()
        pygame.display.set_mode((1, 1))
        pygame.key.set_repeat(100, 100)

        with Receiver() as r:
            print("Connection established")
            time.sleep(1)
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    r.send_command("stop")
                else:
                    r.send_command(KEY_TEXT[event.key])
    except KeyboardInterrupt:
        sys.exit(0)
