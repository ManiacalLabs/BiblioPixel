from distutils.version import LooseVersion
from . codes import CMDTYPE, LEDTYPE, SPIChipsets, BufferChipsets
from ... return_codes import RETURN_CODES, print_error
from ... import log, util

try:
    import serial
    import serial.tools.list_ports
except ImportError as e:
    error = "Please install pyserial 2.7+! pip install pyserial"
    log.error(error)
    raise ImportError(error)

if LooseVersion(serial.VERSION) < LooseVersion('2.7'):
    error = "pyserial v{} found, please upgrade to v2.7+! pip install pyserial --upgrade".format(
        serial.VERSION)
    log.error(error)
    raise ImportError(error)


class Devices(object):
    """Manage a list of serial devices."""

    def __init__(self):
        self.foundDevices = []
        self.deviceIDS = {}
        self.deviceVers = []

    def findSerialDevices(self, hardwareID="1D50:60AB", baudrate=921600):
        hardwareID = "(?i)" + hardwareID  # forces case insensitive
        if len(self.foundDevices) == 0:
            self.foundDevices = []
            self.deviceIDS = {}
            for port in serial.tools.list_ports.grep(hardwareID):
                id = self.getDeviceID(port[0], baudrate)
                ver = self.getDeviceVer(port[0], baudrate)
                if id >= 0:
                    self.deviceIDS[id] = port[0]
                    self.foundDevices.append(port[0])
                    self.deviceVers.append(ver)

        return self.foundDevices

    def error(self):
        error = "There was an unknown error communicating with the device."
        log.error(error)
        raise IOError(error)

    def setDeviceID(self, dev, id, baudrate=921600):
        if id < 0 or id > 255:
            raise ValueError("ID must be an unsigned byte!")

        try:
            com = serial.Serial(dev, baudrate=baudrate, timeout=5)

            packet = util.generate_header(CMDTYPE.SETID, 1)
            packet.append(id)
            com.write(packet)

            resp = com.read(1)
            if len(resp) == 0:
                self.error()
            else:
                if ord(resp) != RETURN_CODES.SUCCESS:
                    print_error(ord(resp))

        except serial.SerialException:
            log.error("Problem connecting to serial device.")
            raise IOError("Problem connecting to serial device.")

    def getDeviceID(self, dev, baudrate=921600):
        packet = util.generate_header(CMDTYPE.GETID, 0)
        try:
            com = serial.Serial(dev, baudrate=baudrate, timeout=5)
            com.write(packet)
            resp = ord(com.read(1))
            return resp
        except serial.SerialException:
            log.error("Problem connecting to serial device.")
            return -1

    def getDeviceVer(self, dev, baudrate=921600):
        packet = util.generate_header(CMDTYPE.GETVER, 0)
        try:
            com = serial.Serial(dev, baudrate=baudrate, timeout=0.5)
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
