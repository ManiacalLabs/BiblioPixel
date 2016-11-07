from driver_base import DriverBase
import socket
import sys
import time
import struct

import os
os.sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import log


class CMDTYPE:
    SETUP_DATA = 1  # reserved for future use
    PIXEL_DATA = 2
    BRIGHTNESS = 3


class RETURN_CODES:
    SUCCESS = 255  # All is well
    ERROR = 0  # Generic error
    ERROR_SIZE = 1  # Data receieved does not match given command length
    ERROR_UNSUPPORTED = 2  # Unsupported command


class DriverNetworkUDP(DriverBase):
    """Driver for communicating with another device on the network."""

    def __init__(self, num=0, width=0, height=0, host="localhost", broadcast=False, port=3142, broadcast_interface=''):
        super(DriverNetworkUDP, self).__init__(num, width, height)

        self._host = host
        self._port = port
        self._sock = None
        self._broadcast = broadcast
        self._broadcast_interface = broadcast_interface

    def _generateHeader(self, cmd, size):
        packet = bytearray()
        packet.append(cmd)
        packet.append(size & 0xFF)
        packet.append(size >> 8)
        return packet

# s = socket(AF_INET, SOCK_DGRAM)
# s.bind(('', 0))
# s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    def _connect(self):
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            if self._broadcast:
                # self._sock.bind((self._broadcast_interface, self._port))
                self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

            return self._sock
        except socket.gaierror:
            error = "Unable to connect to or resolve host: {}".format(
                self._host)
            log.error(error)
            raise IOError(error)

    # Push new data to strand
    def update(self, data):
        try:
            s = self._connect()

            count = self.bufByteCount
            packet = self._generateHeader(CMDTYPE.PIXEL_DATA, count)

            packet.extend(data)

            s.sendto(packet, (self._host, self._port))

            s.close()

        except Exception as e:
            log.exception(e)
            error = "Problem communicating with network receiver!"
            log.error(error)
            raise IOError(error)
