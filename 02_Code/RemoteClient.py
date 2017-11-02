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

class Receiver(Thread):

    def __init__(self):
        # TODO: No globals. Eliminate the need by returning it.
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        debug("Connecting...")
        try:
            self.sock.connect((IP_ADDRESS, IP_PORT))
        except socket.gaierror as error:
            debug("Connection failed.")
            raise RuntimeError(
                "Connection to {}:{:d} failed".format(IP_ADDRESS, IP_PORT))
        startReceiver()

    def run(self):
        debug("Receiver thread started")
        while True:
            try:
                rx_data = self.readServerData()
            except:
                debug("Exception in Receiver.run()")
                self.closeConnection()
                break

        debug("Receiver thread terminated")


    def readServerData(self):
        debug("Calling readResponse")
        bufSize = 4096
        data = ""
        while data[-1:] != "\0": # reply with end-of-message indicator
            try:
                blk = sock.recv(bufSize)
                if blk != None:
                    debug("Received data block from server, len: " + \
                        str(len(blk)))
                else:
                    debug("sock.recv() returned with None")
            except:
                raise Exception("Exception from blocking sock.recv()")
            data += blk
        print "Data received:", data

    # TODO: PEP8
    def closeConnection(self):
        debug("Closing socket")
        self.sock.close()

def startReceiver():
    debug("Starting Receiver thread")
    receiver = Receiver()
    receiver.start()

# TODO: Escape need for global by passing in connection to send command to
def sendCommand(cmd, receiver):
    debug("sendCommand() with cmd = " + cmd)
    try:
        # append \0 as end-of-message indicator
        sock.sendall(cmd + "\0")
    except:
        debug("Exception in sendCommand()")
        receiver.closeConnection()




if __name__ == "__main__":
    try:

        sock = None
        isConnected = False

        pygame.init()
        pygame.display.set_mode((1,1))
        pygame.key.set_repeat(100, 100)

        r = Receiver()
        # TODO: PEP8
        isConnected = True
        print "Connection established"
        time.sleep(1)
        while isConnected:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        sendCommand("forward", r)
                    elif event.key == pygame.K_DOWN:
                        sendCommand("reverse", r)
                    elif event.key == pygame.K_LEFT:
                        sendCommand("left", r)
                    elif event.key == pygame.K_RIGHT:
                        sendCommand("right", r)
                if event.type == pygame.KEYUP:
                    sendCommand("stop", r)
    except (KeyboardInterrupt, SystemExit):
        r.closeConnection()
        sys.exit(0)

