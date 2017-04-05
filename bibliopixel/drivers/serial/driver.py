import os, sys, time, traceback

from . codes import CMDTYPE, LEDTYPE, SPIChipsets, BufferChipsets
from . devices import Devices, serial
from .. driver_base import DriverBase, ChannelOrder
from ... import gamma, log, util
from ... return_codes import RETURN_CODES, print_error, BiblioSerialError

DEVICES = Devices()


class DriverSerial(DriverBase):
    """Main driver for Serial based LED strips"""

    def __init__(self, type, num, dev="",
                 c_order=ChannelOrder.RGB, SPISpeed=2,
                 gamma=None, restart_timeout=3,
                 deviceID=None, hardwareID="1D50:60AB",
                 baudrate=921600):
        super().__init__(num, c_order=c_order, gamma=gamma)

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
        self._sync_packet = util.generate_header(CMDTYPE.SYNC, 0)

        if self.deviceID is not None and (self.deviceID < 0 or self.deviceID > 255):
            raise ValueError("deviceID must be between 0 and 255")

        resp = self._connect(baudrate)
        if resp == RETURN_CODES.REBOOT:  # reboot needed
            log.info(
                "Reconfigure and reboot needed, waiting for controller to restart...")
            self._com.close()
            time.sleep(restart_timeout)
            resp = self._connect(baudrate)
            if resp != RETURN_CODES.SUCCESS:
                print_error(resp)
            else:
                log.info("Reconfigure success!")
        elif resp != RETURN_CODES.SUCCESS:
            print_error(resp)

        if type in SPIChipsets:
            log.info("Using SPI Speed: %sMHz", self._SPISpeed)

    def cleanup(self):
        if self._com:
            log.info("Closing connection to: %s", self.dev)
            self._com.close()

    def _connect(self, baudrate):
        try:
            if(self.dev == "" or self.dev is None):
                DEVICES.findSerialDevices(self._hardwareID, baudrate)

                if self.deviceID is not None:
                    if self.deviceID in DEVICES.deviceIDS:
                        self.dev = DEVICES.deviceIDS[self.deviceID]
                        self.devVer = 0
                        try:
                            i = DEVICES.foundDevices.index(self.dev)
                            self.devVer = DEVICES.deviceVers[i]
                        except:
                            pass
                        log.info("Using COM Port: %s, Device ID: %s, Device Ver: %s",
                                 self.dev, self.deviceID, self.devVer)

                    if self.dev == "" or self.dev is None:
                        error = "Unable to find device with ID: {}".format(
                            self.deviceID)
                        log.error(error)
                        raise ValueError(error)
                elif len(DEVICES.foundDevices) > 0:
                    self.dev = DEVICES.foundDevices[0]
                    self.devVer = 0
                    try:
                        i = DEVICES.foundDevices.index(self.dev)
                        self.devVer = DEVICES.deviceVers[i]
                    except:
                        pass
                    devID = -1
                    for id in DEVICES.deviceIDS:
                        if DEVICES.deviceIDS[id] == self.dev:
                            devID = id

                    log.info("Using COM Port: %s, Device ID: %s, Device Ver: %s",
                             self.dev, devID, self.devVer)

            try:
                self._com = serial.Serial(self.dev, baudrate=baudrate, timeout=5)
            except serial.SerialException as e:
                ports = DEVICES.findSerialDevices(self._hardwareID, baudrate)
                error = "Invalid port specified. No COM ports available."
                if len(ports) > 0:
                    error = "Invalid port specified. Try using one of: \n" + \
                        "\n".join(ports)
                log.info(error)
                raise BiblioSerialError(error)

            packet = util.generate_header(CMDTYPE.SETUP_DATA, 4)
            packet.append(self._type)  # set strip type
            byteCount = self.bufByteCount()
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
                DEVICES.error()

            return ord(resp)

        except serial.SerialException as e:
            error = ("Unable to connect to the device. Please check that "
                     "it is connected and the correct port is selected.")
            log.error(traceback.format_exc())
            log.error(error)
            raise e

    def set_brightness(self, brightness):
        super().set_brightness(brightness)
        packet = util.generate_header(CMDTYPE.BRIGHTNESS, 1)
        packet.append(self._brightness)
        self._com.write(packet)
        resp = ord(self._com.read(1))
        if resp == RETURN_CODES.SUCCESS:
            return True
        print_error(resp)

    def _send_packet(self):
        self._com.write(self._packet)

        resp = self._com.read(1)
        if len(resp) == 0:
            DEVICES.error()
        if ord(resp) != RETURN_CODES.SUCCESS:
            print_error(ord(resp))

        self._com.flushInput()

    def _compute_packet(self):
        count = self.bufByteCount() + self._bufPad
        self._packet = util.generate_header(CMDTYPE.PIXEL_DATA, count)

        self._render()

        self._packet.extend(self._buf)
        self._packet.extend([0] * self._bufPad)

    def _send_sync(self):
        self._com.write(self._sync_packet)


class DriverTeensySmartMatrix(DriverSerial):
    def __init__(self, width, height, dev="", deviceID=None,
                 hardwareID="16C0:0483"):
        super().__init__(type=LEDTYPE.GENERIC, num=width * height,
                         deviceID=deviceID, hardwareID=hardwareID)
        self.sync = self._send_sync


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
