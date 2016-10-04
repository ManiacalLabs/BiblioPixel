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

    def __init__(self, num=0, width=0, height=0, multicast=False, host="localhost", port=3142):
        super(DriverNetworkUDP, self).__init__(num, width, height)

        self._host = host
        self._port = port
        self._sock = None
        self._multicast = multicast

    def _generateHeader(self, cmd, size):
        packet = bytearray()
        packet.append(cmd)
        packet.append(size & 0xFF)
        packet.append(size >> 8)
        return packet

    def _connect(self):
        try:
            if self._multicast:
                self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                ttl = struct.pack('b', 1)
                self._sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
            else:
                self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
