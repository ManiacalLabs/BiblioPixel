from driver_base import DriverBase, ChannelOrder
import sys
import time
import os
from .. import gamma, log
import traceback
try:
    import serial
    import serial.tools.list_ports
except ImportError as e:
    error = "Please install pyserial 2.7+! pip install pyserial"
    log.error(error)
    raise ImportError(error)

from distutils.version import LooseVersion

if LooseVersion(serial.VERSION) < LooseVersion('2.7'):
    error = "pyserial v{} found, please upgrade to v2.7+! pip install pyserial --upgrade".format(
        serial.VERSION)
    log.error(error)
    raise ImportError(error)


class BiblioSerialError(Exception):
    pass


class CMDTYPE:
    SETUP_DATA = 1  # config data (LED type, SPI speed, num LEDs)
    PIXEL_DATA = 2  # raw pixel data will be sent as [R1,G1,B1,R2,G2,B2,...]
    BRIGHTNESS = 3  # data will be single 0-255 brightness value, length must be 0x00,0x01
    GETID = 4
    SETID = 5
    GETVER = 6
    SYNC = 7


class RETURN_CODES:
    SUCCESS = 255  # All is well
    REBOOT = 42  # Device reboot needed after configuration
    ERROR = 0  # Generic error
    ERROR_SIZE = 1  # Data receieved does not match given command length
    ERROR_UNSUPPORTED = 2  # Unsupported command
    ERROR_PIXEL_COUNT = 3  # Too many pixels for device
    ERROR_BAD_CMD = 4  # Unknown Command


class LEDTYPE:
    GENERIC = 0  # Use if the serial device only supports one chipset
    LPD8806 = 1
    WS2801 = 2
    # These are all the same
    WS2811 = 3
    WS2812 = 3
    WS2812B = 3
    NEOPIXEL = 3
    APA104 = 3
    # 400khz variant of above
    WS2811_400 = 4

    TM1809 = 5
    TM1804 = 5
    TM1803 = 6
    UCS1903 = 7
    SM16716 = 8
    APA102 = 9
    LPD1886 = 10
    P9813 = 11

SPIChipsets = [
    LEDTYPE.LPD8806,
    LEDTYPE.WS2801,
    LEDTYPE.SM16716,
    LEDTYPE.APA102,
    LEDTYPE.P9813
]

# Chipsets here require extra pixels padded at the end
# Key must be an LEDTYPE
# value a lambda function to calc the value based on numLEDs
BufferChipsets = {
    LEDTYPE.APA102: lambda num: (int(num / 64.0) + 1)
}


class DriverSerial(DriverBase):
    """Main driver for Serial based LED strips"""
    foundDevices = []
    deviceIDS = {}
    deviceVers = []

    def __init__(self, type, num, dev="", c_order=ChannelOrder.RGB, SPISpeed=2, gamma=None, restart_timeout=3, deviceID=None, hardwareID="1D50:60AB"):
        super(DriverSerial, self).__init__(num, c_order=c_order, gamma=gamma)

        if SPISpeed < 1 or SPISpeed > 24 or not (type in SPIChipsets):
            SPISpeed = 1

        self._hardwareID = hardwareID
        self._SPISpeed = SPISpeed
        self._com = None
        self._type = type
        self._bufPad = 0
        self.dev = dev
        self.devVer = 0
        self.deviceID = deviceID
        if self.deviceID is not None and (self.deviceID < 0 or self.deviceID > 255):
            raise ValueError("deviceID must be between 0 and 255")

        resp = self._connect()
        if resp == RETURN_CODES.REBOOT:  # reboot needed
            log.info(
                "Reconfigure and reboot needed, waiting for controller to restart...")
            self._com.close()
            time.sleep(restart_timeout)
            resp = self._connect()
            if resp != RETURN_CODES.SUCCESS:
                DriverSerial._printError(resp)
            else:
                log.info("Reconfigure success!")
        elif resp != RETURN_CODES.SUCCESS:
            DriverSerial._printError(resp)

        if type in SPIChipsets:
            log.info("Using SPI Speed: %sMHz", self._SPISpeed)

    def __exit__(self, type, value, traceback):
        if self._com is not None:
            log.info("Closing connection to: %s", self.dev)
            self._com.close()

    @staticmethod
    def findSerialDevices(hardwareID="1D50:60AB"):
        hardwareID = "(?i)" + hardwareID  # forces case insensitive
        if len(DriverSerial.foundDevices) == 0:
            DriverSerial.foundDevices = []
            DriverSerial.deviceIDS = {}
            for port in serial.tools.list_ports.grep(hardwareID):
                id = DriverSerial.getDeviceID(port[0])
                ver = DriverSerial.getDeviceVer(port[0])
                if id >= 0:
                    DriverSerial.deviceIDS[id] = port[0]
                    DriverSerial.foundDevices.append(port[0])
                    DriverSerial.deviceVers.append(ver)

        return DriverSerial.foundDevices

    @staticmethod
    def _printError(error):
        msg = "Unknown error occured."
        if error == RETURN_CODES.ERROR_SIZE:
            msg = "Data packet size incorrect."
        elif error == RETURN_CODES.ERROR_UNSUPPORTED:
            msg = "Unsupported configuration attempted."
        elif error == RETURN_CODES.ERROR_PIXEL_COUNT:
            msg = "Too many pixels specified for device."
        elif error == RETURN_CODES.ERROR_BAD_CMD:
            msg = "Unsupported protocol command. Check your device version."

        log.error("%s: %s", error, msg)
        raise BiblioSerialError(msg)

    @staticmethod
    def _comError():
        error = "There was an unknown error communicating with the device."
        log.error(error)
        raise IOError(error)

    def _connect(self):
        try:
            if(self.dev == "" or self.dev is None):
                DriverSerial.findSerialDevices(self._hardwareID)

                if self.deviceID is not None:
                    if self.deviceID in DriverSerial.deviceIDS:
                        self.dev = DriverSerial.deviceIDS[self.deviceID]
                        self.devVer = 0
                        try:
                            i = DriverSerial.foundDevices.index(self.dev)
                            self.devVer = DriverSerial.deviceVers[i]
                        except:
                            pass
                        log.info("Using COM Port: %s, Device ID: %s, Device Ver: %s",
                                 self.dev, self.deviceID, self.devVer)

                    if self.dev == "" or self.dev is None:
                        error = "Unable to find device with ID: {}".format(
                            self.deviceID)
                        log.error(error)
                        raise ValueError(error)
                elif len(DriverSerial.foundDevices) > 0:
                    self.dev = DriverSerial.foundDevices[0]
                    self.devVer = 0
                    try:
                        i = DriverSerial.foundDevices.index(self.dev)
                        self.devVer = DriverSerial.deviceVers[i]
                    except:
                        pass
                    devID = -1
                    for id in DriverSerial.deviceIDS:
                        if DriverSerial.deviceIDS[id] == self.dev:
                            devID = id

                    log.info("Using COM Port: %s, Device ID: %s, Device Ver: %s",
                             self.dev, devID, self.devVer)

            try:
                self._com = serial.Serial(self.dev, timeout=5)
            except serial.SerialException as e:
                ports = DriverSerial.findSerialDevices(self._hardwareID)
                error = "Invalid port specified. No COM ports available."
                if len(ports) > 0:
                    error = "Invalid port specified. Try using one of: \n" + \
                        "\n".join(ports)
                log.info(error)
                raise BiblioSerialError(error)

            packet = DriverSerial._generateHeader(CMDTYPE.SETUP_DATA, 4)
            packet.append(self._type)  # set strip type
            byteCount = self.bufByteCount
            if self._type in BufferChipsets:
                if self._type == LEDTYPE.APA102 and self.devVer >= 2:
                    pass
                else:
                    self._bufPad = BufferChipsets[self._type](self.numLEDs) * 3
                    byteCount += self._bufPad

            packet.append(byteCount & 0xFF)  # set 1st byte of byteCount
            packet.append(byteCount >> 8)  # set 2nd byte of byteCount
            packet.append(self._SPISpeed)
            self._com.write(packet)

            resp = self._com.read(1)
            if len(resp) == 0:
                DriverSerial._comError()

            return ord(resp)

        except serial.SerialException as e:
            error = "Unable to connect to the device. Please check that it is connected and the correct port is selected."
            log.error(traceback.format_exc())
            log.error(error)
            raise e

    @staticmethod
    def _generateHeader(cmd, size):
        packet = bytearray()
        packet.append(cmd)
        packet.append(size & 0xFF)
        packet.append(size >> 8)
        return packet

    @staticmethod
    def setDeviceID(dev, id):
        if id < 0 or id > 255:
            raise ValueError("ID must be an unsigned byte!")

        try:
            com = serial.Serial(dev, timeout=5)

            packet = DriverSerial._generateHeader(CMDTYPE.SETID, 1)
            packet.append(id)
            com.write(packet)

            resp = com.read(1)
            if len(resp) == 0:
                DriverSerial._comError()
            else:
                if ord(resp) != RETURN_CODES.SUCCESS:
                    DriverSerial._printError(ord(resp))

        except serial.SerialException:
            log.error("Problem connecting to serial device.")
            raise IOError("Problem connecting to serial device.")

    @staticmethod
    def getDeviceID(dev):
        packet = DriverSerial._generateHeader(CMDTYPE.GETID, 0)
        try:
            com = serial.Serial(dev, timeout=5)
            com.write(packet)
            resp = ord(com.read(1))
            return resp
        except serial.SerialException:
            log.error("Problem connecting to serial device.")
            return -1

    @staticmethod
    def getDeviceVer(dev):
        packet = DriverSerial._generateHeader(CMDTYPE.GETVER, 0)
        try:
            com = serial.Serial(dev, timeout=0.5)
            com.write(packet)
            ver = 0
            resp = com.read(1)
            if len(resp) > 0:
                resp = ord(resp)
                if resp == RETURN_CODES.SUCCESS:
                    ver = ord(com.read(1))
            return ver
        except serial.SerialException:
            log.error("Problem connecting to serial device.")
            return 0

    def setMasterBrightness(self, brightness):
        packet = DriverSerial._generateHeader(CMDTYPE.BRIGHTNESS, 1)
        packet.append(brightness)
        self._com.write(packet)
        resp = ord(self._com.read(1))
        if resp != RETURN_CODES.SUCCESS:
            DriverSerial._printError(resp)
            return False
        else:
            return True

    # Push new data to strand
    def update(self, data):
        count = self.bufByteCount + self._bufPad
        packet = DriverSerial._generateHeader(CMDTYPE.PIXEL_DATA, count)

        self._fixData(data)

        packet.extend(self._buf)
        packet.extend([0] * self._bufPad)
        self._com.write(packet)

        resp = self._com.read(1)
        if len(resp) == 0:
            DriverSerial._comError()
        if ord(resp) != RETURN_CODES.SUCCESS:
            DriverSerial._printError(ord(resp))

        self._com.flushInput()

    def _sync(self):
        packet = DriverSerial._generateHeader(CMDTYPE.SYNC, 0)
        self._com.write(packet)
        resp = self._com.read(1)
        if len(resp) == 0:
            DriverSerial._comError()
        if ord(resp) != RETURN_CODES.SUCCESS:
            DriverSerial._printError(ord(resp))

        self._com.flushInput()


class DriverTeensySmartMatrix(DriverSerial):
    def __init__(self, width, height, dev="", deviceID=None, hardwareID="16C0:0483"):
        super(DriverTeensySmartMatrix, self).__init__(type=LEDTYPE.GENERIC, num=width * height, deviceID=deviceID, hardwareID=hardwareID)
        self.sync = self._sync


MANIFEST = [
    {
        "id": "serial",
        "class": DriverSerial,
        "type": "driver",
        "display": "Serial (AllPixel)",
        "desc": "Interface with USB Serial devices that support the AllPixel protocol.",
        "params": [{
                "id": "type",
                "label": "LED Type",
                "type": "combo",
                "options": {
                    0: "GENERIC",
                    1: "LPD8806",
                    2: "WS2801",
                    3: "WS281x/NEOPIXEL",
                    4: "WS2811_400",
                    5: "TM1804",
                    6: "TM1803",
                    7: "UCS1903",
                    8: "SM16716",
                    9: "APA102",
                    10: "LPD1886",
                    11: "P98131"
                },
            "default": 0
        }, {
            "id": "num",
            "label": "# Pixels",
            "type": "int",
            "default": 0,
            "min": 0,
            "help": "Total pixels in display."
        }, {
            "id": "dev",
            "label": "Device Path",
            "type": "str",
            "default": "",
        }, {
            "id": "c_order",
            "label": "Channel Order",
            "type": "combo",
            "options": {
                    0: "RGB",
                    1: "RBG",
                    2: "GRB",
                    3: "GBR",
                    4: "BRG",
                    5: "BGR"
            },
            "options_map": [
                [0, 1, 2],
                [0, 2, 1],
                [1, 0, 2],
                [1, 2, 0],
                [2, 0, 1],
                [2, 1, 0]
            ],
            "default": 0
        }, {
            "id": "SPISpeed",
            "label": "SPI Speed (MHz)",
            "type": "int",
            "default": 2,
            "min": 1,
            "max": 24,
            "group": "Advanced"
        }, {
            "id": "gamma",
            "label": "Gamma",
            "type": "combo",
            "default": None,
            "options": {
                    0: "LPD8806",
                    1: "APA102",
                    2: "WS2801",
                    3: "SM16716",
                    5: "WS281x"
            },
            "options_map": [
                gamma.LPD8806,
                gamma.APA102,
                gamma.WS2801,
                gamma.SM16716,
                gamma.WS2812B
            ]
        }, {
            "id": "restart_timeout",
            "label": "Restart Timeout",
            "type": "int",
            "default": 3,
            "min": 1,
            "group": "Advanced"
        }, {
            "id": "deviceID",
            "label": "Device ID",
            "type": "int",
            "default": None,
            "min": 0,
            "max": 255,
            "msg": "AllPixel ID",
            "group": "Advanced"
        }, {
            "id": "hardwareID",
            "label": "Hardware ID",
            "type": "str",
            "default": "1D50:60AB",
            "group": "Advanced"
        }, ]
    },
    {
        "id": "teensysmartmatrix",
        "class": DriverTeensySmartMatrix,
        "type": "driver",
        "display": "Teensy SmartMatrix",
        "desc": "Interface with Teensy SmartMatrix Controller.",
        "params": [{
            "id": "width",
            "label": "Width",
            "type": "int",
            "default": 32,
            "min": 16,
            "help": "Width of display. Firmware hardcoded."
        }, {
            "id": "height",
            "label": "Height",
            "type": "int",
            "default": 32,
            "min": 16,
            "help": "Width of display. Firmware hardcoded."
        }, {
            "id": "dev",
            "label": "Device Path",
            "type": "str",
            "default": "",
        }, {
            "id": "deviceID",
            "label": "Device ID",
            "type": "int",
            "default": None,
            "min": 0,
            "max": 255,
            "msg": "Teensy ID",
            "group": "Advanced"
        }, {
            "id": "hardwareID",
            "label": "Hardware ID",
            "type": "str",
            "default": "16C0:0483",
            "group": "Advanced"
        }, ]
    }
]
