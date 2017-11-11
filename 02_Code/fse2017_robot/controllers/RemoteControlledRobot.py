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

"""Server to run on a robot which is remotely controlled by network."""

import socket
from logging import debug
from threading import Thread

from ..robot import Robot

IP_PORT = 22000


class SocketHandler(Thread):
    """Server to handle incoming commands from remote control agent."""

    command_terminator = "\0"

    def __init__(self, conn, robot):
        Thread.__init__(self)
        self.conn = conn
        self.connected = False
        self.robot = robot

    def run(self):
        debug("SocketHandler started")
        while True:
            cmd = ""
            try:
                cmd = self.conn.recv(1024)
            except socket.error:
                debug("Connection was reset by peer.")
                break
            debug("Received cmd: " + cmd + " len: " + str(len(cmd)))
            if not len(cmd):
                break
            self.execute(cmd)
        connection.close()
        print("Client disconnected. Waiting for next client...")
        self.connected = False
        debug("SocketHandler terminated")

    def execute(self, cmd):
        print("Reporting current state: {}".format(cmd))
        self.conn.sendall(cmd)
        self.conn.sendall(cmd)

        if cmd == "forward":
            self.robot.motor.forward()
        elif cmd == "reverse":
            self.robot.motor.reverse()
        elif cmd == "left":
            self.robot.motor.left()
        elif cmd == "right":
            self.robot.motor.right()
        elif cmd == "stop":
            self.robot.motor.stop()
        else:
            self.robot.motor.stop()


if __name__ == "__main__":
    with Robot() as r:
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Close port when process exits
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            debug("Socket created")
            HOSTNAME = ""  # Symbolic name for all available interfaces
            server_socket.bind((HOSTNAME, IP_PORT))
            server_socket.listen(10)
            print("Waiting for a connecting client...")

            while True:
                debug("Calling blocking accept()...")
                connection, address = server_socket.accept()
                print("Connected with client at " + address[0])
                socketHandler = SocketHandler(connection, r)
                # Terminate socket handler with parent thread
                socketHandler.setDaemon(True)
                socketHandler.start()
