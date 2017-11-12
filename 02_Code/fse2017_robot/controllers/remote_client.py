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

"""Client for sending commands to remote server controlling robot."""

import socket
import time
from logging import debug
from threading import Thread

import pygame

IP_ADDRESS = "192.168.0.102"
IP_PORT = 22000

KEY_TEXT = {
    pygame.K_UP: "forward",
    pygame.K_DOWN: "reverse",
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right"
}


class KeyListener(Thread):
    """Listener for key entries."""

    BUFFER_SIZE = 4096
    END_OF_MESSAGE_INDICATOR = "\0"

    def __init__(self):
        """Try to establish connection to remote server."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        debug("Connecting...")
        try:
            self.sock.connect((IP_ADDRESS, IP_PORT))
            self.connected = True
        except socket.gaierror as error:
            debug("Connection failed.")
            raise RuntimeError(
                "Connection to {}:{:d} failed".format(IP_ADDRESS, IP_PORT))

    def send_command(self, cmd):
        """Send text to remote server."""
        debug("sendCommand() with cmd = " + cmd)
        try:
            self.sock.sendall(cmd + self.END_OF_MESSAGE_INDICATOR)
        except socket.error:
            debug("Exception in sendCommand()")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        debug("Closing socket")
        self.connected = False
        self.sock.close()


if __name__ == "__main__":
    try:
        pygame.init()
        pygame.display.set_mode((1, 1))
        pygame.key.set_repeat(100, 100)

        with KeyListener() as listener:
            print("Connection established")
            time.sleep(1)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYUP:
                        listener.send_command("stop")
                    elif event.type == pygame.KEYDOWN:
                        listener.send_command(KEY_TEXT[event.key])
                    else:
                        pass
    except KeyboardInterrupt:
        pass
