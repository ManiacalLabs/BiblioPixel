from distutils.version import LooseVersion
from .. util import AttributeDict, generate_header, log
import serial, serial.tools.list_ports
from .. drivers.return_codes import RETURN_CODES, print_error
from . gamepad import BaseGamePad

VERSION_ERROR = """
pyserial v{} found, please upgrade to v2.7+!
    pip install pyserial --upgrade
"""

UNABLE_TO_CONNECT_ERROR = """
Unable to connect to the device.
Please check that it is connected and the correct port is selected.
"""

if LooseVersion(serial.VERSION) < LooseVersion('2.7'):
    error = VERSION_ERROR.format(serial.VERSION)
    log.error(error)
    raise ImportError(error)

BTN_MAP = ('A', 'B', 'SELECT', 'START', 'UP', 'DOWN', 'LEFT', 'RIGHT', 'X', 'Y')


class CMDTYPE:
    INIT = 0
    GET_BTNS = 1
    SET_LEDS = 2
    SET_MODE = 4


class SerialPadError(Exception):
    pass


class SerialGamePad(BaseGamePad):
    devices = []

    def __init__(self, btn_map=BTN_MAP, dev="", hardwareID="1B4F:9206"):
        super().__init__()
        self._map = btn_map
        self._hardwareID = hardwareID
        self._com = None
        self.dev = dev

        resp = self._connect()
        if resp != RETURN_CODES.SUCCESS:
            raise SerialPadError(print_error(resp))

    def cleanup(self):
        if self._com is not None:
            log.info("Closing connection to: %s", self.dev)
            self._com.close()

    def close(self):
        from .. util import deprecated
        deprecated.deprecated('SerialGamePad.close')
        self.cleanup()

    @staticmethod
    def find_serial_devices(hardwareID="1B4F:9206"):
        hardwareID = "(?i)" + hardwareID  # forces case insensitive
        if len(SerialGamePad.devices) == 0:
            SerialGamePad.devices = []
            for port in serial.tools.list_ports.grep(hardwareID):
                SerialGamePad.devices.append(port[0])

        return SerialGamePad.devices

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
    def _comError(fail=False):
        error = "There was an unknown error communicating with the device."
        log.error(error)
        if fail:
            raise IOError(error)

    def _connect(self):
        try:
            if(self.dev == ""):
                SerialGamePad.find_serial_devices(self._hardwareID)

                if len(SerialGamePad.devices) > 0:
                    self.dev = SerialGamePad.devices[0]
                    log.info("Using COM Port: %s", self.dev)

            try:
                self._com = serial.Serial(self.dev, timeout=5)
            except serial.SerialException as e:
                ports = SerialGamePad.find_serial_devices(self._hardwareID)
                error = "Invalid port specified. No COM ports available."
                if len(ports) > 0:
                    error = "Invalid port specified. Try using one of: \n" + \
                        "\n".join(ports)
                log.info(error)
                raise SerialPadError(error)

            packet = generate_header(CMDTYPE.INIT, 0)
            self._com.write(packet)

            resp = self._com.read(1)
            return resp and ord(resp)

        except serial.SerialException as e:
            error = UNABLE_TO_CONNECT_ERROR
            log.exception(e)
            log.error(error)
            raise e

    def getKeys(self):
        bits = 0
        try:
            packet = generate_header(CMDTYPE.GET_BTNS, 0)
            self._com.write(packet)
            resp = self._com.read(1)

            if len(resp) == 0:
                SerialGamePad._comError()
            elif ord(resp) != RETURN_CODES.SUCCESS:
                print_error(ord(resp))
            else:
                resp = self._com.read(2)
                if len(resp) != 2:
                    SerialGamePad._comError()
                else:
                    bits = ord(resp[0]) + (ord(resp[1]) << 8)
        except:
            log.error("IO Error Communicating With Game Pad!")

        index = 0
        result = {}
        for m in self._map:
            result[m] = (bits & (1 << index) > 0)
            index += 1
        return AttributeDict(result)

    def setLights(self, data):
        temp = [(0, 0, 0)] * len(data.keys())
        for key in data:
            i = self._map.index(key)
            if i >= 0 and i < len(temp):
                temp[i] = (data[key])
        leds = []
        for l in temp:
            leds.extend(l)

        packet = generate_header(CMDTYPE.SET_LEDS, len(leds))
        packet.extend(leds)
        self._com.write(packet)
        resp = self._com.read(1)
        if len(resp) == 0:
            SerialGamePad._comError()
        elif ord(resp) != RETURN_CODES.SUCCESS:
            print_error(ord(resp))

    def setLightsOff(self, count):
        data = {}
        num = 0
        for b in self._map:
            data[b] = (0, 0, 0)
            num += 1
            if num >= count:
                break
        self.setLights(data)
