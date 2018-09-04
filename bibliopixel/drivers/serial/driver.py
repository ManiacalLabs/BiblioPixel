import os, sys, serial, time, traceback

from . codes import CMDTYPE, LEDTYPE, SPIChipsets, BufferChipsets
from . devices import Devices
from . import io
from .. channel_order import ChannelOrder
from .. driver_base import DriverBase
from ... util import log, util
from ... drivers.return_codes import (
    RETURN_CODES, print_error, raise_error, BiblioSerialError)


class Serial(DriverBase):
    """Main driver for Serial based LED strips and devices like the AllPixel

    Provides the same parameters of
    :py:class:`bibliopixel.drivers.driver_base.DriverBase` as
    well as those below:

    :param ledtype: LED protocol type. One of
        :py:func:`bibliopixel.drivers.ledtype.LEDTYPE`
    :param str dev: Serial device address/path. If left empty, first device
        found will be used.
    :param int spi_speed: SPI datarate for applicable LED types, in MHz
    :param int restart_timeout: Seconds to wait between reconfigure reboot
        and reconnection attempt
    :param int device_id: Device ID to connect to.
    :param str hardwareID: A valid USB VID:PID pair such as "1D50:60AB"
    :param int baudrate: Baud rate to connect to serial device
    """

    def __init__(self, ledtype=None, num=0, dev="",
                 c_order='RGB', spi_speed=2,
                 gamma=None, restart_timeout=3,
                 device_id=None, hardwareID="1D50:60AB",
                 baudrate=921600, **kwds):

        if ledtype is None:
            raise ValueError('Must provide ledtype value!')

        if num == 0:
            raise ValueError('Must provide num value >0!')

        super().__init__(num, c_order=c_order, gamma=gamma, **kwds)
        self.devices = Devices(hardwareID, baudrate)

        if not (1 <= spi_speed <= 24 and ledtype in SPIChipsets):
            spi_speed = 1

        self._spi_speed = spi_speed
        self._com = None
        self._ledtype = ledtype
        self._bufPad = 0
        self.dev = dev
        self.device_version = 0
        self.device_id = device_id
        self._sync_packet = util.generate_header(CMDTYPE.SYNC, 0)

        if self.device_id is not None and not (0 <= self.device_id <= 255):
            raise ValueError("device_id must be between 0 and 255")

        resp = self._connect()
        if resp == RETURN_CODES.REBOOT:  # reboot needed
            log.info(REBOOT_MESSAGE)
            self._close()
            time.sleep(restart_timeout)
            resp = self._connect()
            if resp != RETURN_CODES.SUCCESS:
                raise_error(resp)
            else:
                log.info("Reconfigure success!")
        elif resp != RETURN_CODES.SUCCESS:
            raise_error(resp)

        if type in SPIChipsets:
            log.info("Using SPI Speed: %sMHz", self._spi_speed)

    def cleanup(self):
        """
        SHOULD BE PRIVATE
        """
        if self._com:
            log.info("Closing connection to: %s", self.dev)
            self._close()

    def _connect(self):
        try:
            if not self.dev:
                self.devices.find_serial_devices()
                idv = self.devices.get_device(self.device_id)
                self.device_id, self.dev, self.device_version = idv
            try:
                self._com = serial.Serial(
                    self.dev, baudrate=self.devices.baudrate, timeout=5)
            except serial.SerialException as e:
                ports = self.devices.devices.values()
                error = "Invalid port specified. No COM ports available."
                if ports:
                    error = ("Invalid port specified. Try using one of: \n" +
                             "\n".join(ports))
                log.info(error)
                raise BiblioSerialError(error)

            packet = util.generate_header(CMDTYPE.SETUP_DATA, 4)
            packet.append(self._ledtype)  # set strip type
            byteCount = self.bufByteCount()
            if self._ledtype in BufferChipsets:
                if self._ledtype == LEDTYPE.APA102 and self.device_version >= 2:
                    pass
                else:
                    self._bufPad = BufferChipsets[
                        self._ledtype](self.numLEDs) * 3
                    byteCount += self._bufPad

            packet.append(byteCount & 0xFF)  # set 1st byte of byteCount
            packet.append(byteCount >> 8)  # set 2nd byte of byteCount
            packet.append(self._spi_speed)
            self._write(packet)

            code = self._read()
            if code is None:
                self.devices.error()

            return code

        except serial.SerialException as e:
            error = ("Unable to connect to the device. Please check that "
                     "it is connected and the correct port is selected.")
            log.error(traceback.format_exc())
            log.error(error)
            raise e

    def set_device_brightness(self, brightness):
        packet = util.generate_header(CMDTYPE.BRIGHTNESS, 1)
        packet.append(self._brightness)
        self._write(packet)
        code = self._read()
        if code == RETURN_CODES.SUCCESS:
            return True
        print_error(code)

    def _send_packet(self):
        if not self._com:
            return

        self._write(self._packet)

        code = self._read()
        if code is None:
            self.devices.error(fail=False)
        elif code != RETURN_CODES.SUCCESS:
            print_error(code)
        else:
            self._flushInput()
            return True

    def _compute_packet(self):
        count = self.bufByteCount() + self._bufPad
        self._packet = util.generate_header(CMDTYPE.PIXEL_DATA, count)

        self._render()
        self._packet.extend(self._buf)
        self._packet.extend([0] * self._bufPad)

    def _send_sync(self):
        self._write(self._sync_packet)

    def _read(self):
        return io.read_byte(self._com)

    def _close(self):
        try:
            return self._com and self._com.close()
        except Exception as e:
            log.error('Serial exception %s in close', e)
        finally:
            self._com = None

    def _write(self, packet):
        try:
            return self._com and self._com.write(packet)
        except Exception as e:
            log.error('Serial exception %s in write', e)

    def _flushInput(self):
        try:
            return self._com and self._com.flushInput()
        except Exception as e:
            log.error('Serial exception %s in flushInput', e)


class TeensySmartMatrix(Serial):
    """Variant of :py:class:`Serial` for use with the Teensy and
    SmartMatrix library. The following provides compatible firmware:
    https://github.com/ManiacalLabs/BiblioPixelSmartMatrix

    All parameters are the same as with :py:class:`Serial`, except the
    default hardwareID is changed to match the Teensy.

    The main difference is that SmartMatrix requires a sync command to keep
    multiple instances of this driver running smoothly.
    """

    def __init__(self, width, height, dev="", device_id=None,
                 hardwareID="16C0:0483", **kwds):
        super().__init__(ledtype=LEDTYPE.GENERIC, num=width * height,
                         device_id=device_id, hardwareID=hardwareID, **kwds)
        self.sync = self._send_sync


REBOOT_MESSAGE = """Reconfigure and reboot needed!
Waiting for controller to restart..."""

from ... util import deprecated
if deprecated.allowed():  # pragma: no cover
    DriverSerial = Serial
    DriverTeensySmartMatrix = TeensySmartMatrix
