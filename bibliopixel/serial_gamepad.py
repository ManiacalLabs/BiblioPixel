try:
    import serial
    import serial.tools.list_ports
except ImportError as e:
    error = "Please install pyserial 2.7+! pip install pyserial"
    raise ImportError(error)

from distutils.version import LooseVersion
from util import d
from gamepad import BaseGamePad
import log

if LooseVersion(serial.VERSION) < LooseVersion('2.7'):
    error = "pyserial v{} found, please upgrade to v2.7+! pip install pyserial --upgrade".format(
        serial.VERSION)
    log.error(error)
    raise ImportError(error)


class CMDTYPE:
    INIT = 0
    GET_BTNS = 1
    SET_LEDS = 2
    SET_MODE = 4


class RETURN_CODES:
    SUCCESS = 255
    ERROR = 0
    ERROR_SIZE = 1
    ERROR_UNSUPPORTED = 2
    ERROR_BAD_CMD = 4


class SerialPadError(Exception):
    pass


class SerialGamePad(BaseGamePad):
    foundDevices = []

    def __init__(self, btn_map=["A", "B", "SELECT", "START", "UP", "DOWN", "LEFT", "RIGHT", "X", "Y"], dev="", hardwareID="1B4F:9206"):
        super(SerialGamePad, self).__init__()
        self._map = btn_map
        self._hardwareID = hardwareID
        self._com = None
        self.dev = dev

        resp = self._connect()
        if resp != RETURN_CODES.SUCCESS:
            SerialGamePad._printError(resp)

    def close(self):
        if self._com is not None:
            log.info("Closing connection to: %s", self.dev)
            self._com.close()

    def __exit__(self, type, value, traceback):
        self.close()

    @staticmethod
    def findSerialDevices(hardwareID="1B4F:9206"):
        hardwareID = "(?i)" + hardwareID  # forces case insensitive
        if len(SerialGamePad.foundDevices) == 0:
            SerialGamePad.foundDevices = []
            for port in serial.tools.list_ports.grep(hardwareID):
                SerialGamePad.foundDevices.append(port[0])

        return SerialGamePad.foundDevices

    @staticmethod
    def _printError(error):
        msg = "Unknown error occured."
        if error == RETURN_CODES.ERROR_SIZE:
            msg = "Data packet size incorrect."
        elif error == RETURN_CODES.ERROR_UNSUPPORTED:
            msg = "Unsupported configuration attempted."
        elif error == RETURN_CODES.ERROR_BAD_CMD:
            msg = "Unsupported protocol command. Check your device version."

        log.error("%s: %s", error, msg)
        raise SerialPadError(msg)

    @staticmethod
    def _comError():
        error = "There was an unknown error communicating with the device."
        log.error(error)
        raise IOError(error)

    def _connect(self):
        try:
            if(self.dev == ""):
                SerialGamePad.findSerialDevices(self._hardwareID)

                if len(SerialGamePad.foundDevices) > 0:
                    self.dev = SerialGamePad.foundDevices[0]
                    log.info("Using COM Port: %s", self.dev)

            try:
                self._com = serial.Serial(self.dev, timeout=5)
            except serial.SerialException as e:
                ports = SerialGamePad.findSerialDevices(self._hardwareID)
                error = "Invalid port specified. No COM ports available."
                if len(ports) > 0:
                    error = "Invalid port specified. Try using one of: \n" + \
                        "\n".join(ports)
                log.info(error)
                raise SerialPadError(error)

            packet = SerialGamePad._generateHeader(CMDTYPE.INIT, 0)
            self._com.write(packet)

            resp = self._com.read(1)
            if len(resp) == 0:
                SerialGamePad._comError()

            return ord(resp)

        except serial.SerialException as e:
            error = "Unable to connect to the device. Please check that it is connected and the correct port is selected."
            log.exception(e)
            log.error(error)
            raise e

    @staticmethod
    def _generateHeader(cmd, size):
        packet = bytearray()
        packet.append(cmd)
        packet.append(size & 0xFF)
        packet.append(size >> 8)
        return packet

    def getKeys(self):
        bits = 0
        try:
            packet = SerialGamePad._generateHeader(CMDTYPE.GET_BTNS, 0)
            self._com.write(packet)
            resp = self._com.read(1)

            if len(resp) == 0:
                SerialGamePad._comError()
            elif ord(resp) != RETURN_CODES.SUCCESS:
                SerialGamePad._printError(ord(resp))
            resp = self._com.read(2)
            if len(resp) != 2:
                SerialGamePad._comError()

            bits = ord(resp[0]) + (ord(resp[1]) << 8)
        except IOError:
            log.error("IO Error Communicatng With Game Pad!")

        index = 0
        result = {}
        for m in self._map:
            result[m] = (bits & (1 << index) > 0)
            index += 1
        return d(result)

    def setLights(self, data):
        temp = [(0, 0, 0)] * len(data.keys())
        for key in data:
            i = self._map.index(key)
            if i >= 0 and i < len(temp):
                temp[i] = (data[key])
        leds = []
        for l in temp:
            leds.extend(l)

        packet = SerialGamePad._generateHeader(CMDTYPE.SET_LEDS, len(leds))
        packet.extend(leds)
        self._com.write(packet)
        resp = self._com.read(1)
        if len(resp) == 0:
            SerialGamePad._comError()
        elif ord(resp) != RETURN_CODES.SUCCESS:
            SerialGamePad._printError(ord(resp))

    def setLightsOff(self, count):
        data = {}
        num = 0
        for b in self._map:
            data[b] = (0, 0, 0)
            num += 1
            if num >= count:
                break
        self.setLights(data)

# if __name__ == "__main__":
#     import time
#     pad = SerialGamePad(dev="", hardwareID="1B4F:9206")
#     data = {
#         "A": (255,0,0),
#         "B": (0,255,0),
#         "X": (0,0,255),
#         "Y": (128,0,64),
#         "RED":(255,0,0)
#     }
#     pad.setLights(data)
#     try:
#         count = 0
#         while True:
#             # print count
#             count += 1
#             print pad.getKeys()
#             time.sleep(0.5)
#     except KeyboardInterrupt:
#         pad.setLightsOff(5)
#         pad.__exit__(None, None, None)
