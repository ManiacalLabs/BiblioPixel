from driver_base import DriverBase
import socket
import sys
import time

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


class DriverNetwork(DriverBase):
    """Driver for communicating with another device on the network."""

    def __init__(self, num=0, width=0, height=0, host="localhost", port=3142, persist=False):
        super(DriverNetwork, self).__init__(num, width, height)

        self._host = host
        self._port = port
        self._sock = None
        self.persist = persist

    def _generateHeader(self, cmd, size):
        packet = bytearray()
        packet.append(cmd)
        packet.append(size & 0xFF)
        packet.append(size >> 8)
        return packet

    def _connect(self):
        if self.persist and self._sock:
            return self._sock
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.connect((self._host, self._port))
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

            s.sendall(packet)

            resp = ord(s.recv(1))

            if not self.persist:
                s.close()

            if resp != RETURN_CODES.SUCCESS:
                log.warning("Bytecount mismatch! %s", resp)

        except Exception as e:
            log.exception(e)
            error = "Problem communicating with network receiver!"
            log.error(error)
            raise IOError(error)

    def setMasterBrightness(self, brightness):
        packet = self._generateHeader(CMDTYPE.BRIGHTNESS, 1)
        packet.append(brightness)
        s = self._connect()
        s.sendall(packet)
        resp = ord(s.recv(1))
        if resp != RETURN_CODES.SUCCESS:
            return False
        else:
            return True

MANIFEST = [
    {
        "id": "network",
        "class": DriverNetwork,
        "type": "driver",
        "display": "Network",
        "desc": "Sends pixel data over the network to a reciever.",
        "params": [{
                "id": "num",
                "label": "# Pixels",
                "type": "int",
                "default": 0,
                "min": 0,
                "help": "Total pixels in display. May use Width AND Height instead."
        }, {
            "id": "width",
            "label": "Width",
            "type": "int",
            "default": 0,
            "min": 0,
            "help": "Width of display. Set if using a matrix."
        }, {
            "id": "height",
            "label": "Height",
            "type": "int",
            "default": 0,
            "min": 0,
            "help": "Height of display. Set if using a matrix."
        }, {
            "id": "host",
            "label": "Pixel Size",
            "type": "str",
            "default": "localhost",
            "help": "Receiver host to connect to."
        }, {
            "id": "port",
            "label": "Port",
            "type": "int",
            "default": 3142,
            "help": "Port to connect to."
        }]
    }
]
