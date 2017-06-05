import os, sys, time
from . channel_order import ChannelOrder
from . driver_base import DriverBase
from .. import log


class DriverSPIBase(DriverBase):
    """
    Base driver for controling SPI devices on systems like the Raspberry Pi and
    BeagleBone.
    """
    def __init__(self, num, c_order=ChannelOrder.GRB, use_py_spi=True,
                 dev='/dev/spidev0.0', SPISpeed=2, open=open, gamma=None):
        super().__init__(num, c_order=c_order, gamma=gamma)

        self.dev = dev
        self.use_py_spi = use_py_spi
        self._spiSpeed = SPISpeed
        self._open = open

        # File based SPI requires a bytearray so we have to overwrite _buf
        if self.use_py_spi:
            a, b = -1, -1
            d = self.dev.replace('/dev/spidev', '')
            s = d.split('.')
            if len(s) == 2:
                a = int(s[0])
                b = int(s[1])

            if a < 0 or b < 0:
                error(BAD_FORMAT_ERROR)

            self._bootstrapSPIDev()
            import spidev
            self.spi = spidev.SpiDev()
            self.spi.open(a, b)
            self.spi.max_speed_hz = int(self._spiSpeed * 1000000.0)
            log.info('py-spidev speed @ %.1f MHz',
                     (float(self.spi.max_speed_hz) / 1000000.0))
        else:
            self._buf = bytearray(self._buf)
            self.spi = self._open(self.dev, 'wb')

    def _bootstrapSPIDev(self):
        if self.use_py_spi:
            try:
                import spidev
            except:
                error(CANT_IMPORT_SPIDEV_ERROR)

        if not os.path.exists(self.dev):
            error(CANT_FIND_ERROR)

        # permissions check
        try:
            self._open(self.dev)
        except IOError as e:
            if e.errno == 13:
                error(CANT_FIND_ERROR)
            raise e

    def _send_packet(self):
        if self.use_py_spi:
            self.spi.xfer2(self._packet)
        else:
            self.spi.write(self._packet)
            self.spi.flush()

    def _compute_packet(self):
        self._render()
        self._packet = self._buf


CANT_FIND_ERROR = """Cannot find SPI device.
Please see

    https://github.com/maniacallabs/bibliopixel/wiki/SPI-Setup

for details.
"""

BAD_FORMAT_ERROR = (
    'When using py-spidev, `dev` must be in the format /dev/spidev*.*')

CANT_IMPORT_SPIDEV_ERROR = """
Unable to import spidev. Please install:

    pip install spidev
"""


def error(text):
    log.error(text)
    raise IOError(text)
