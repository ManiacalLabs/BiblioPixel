from driver_base import DriverBase, ChannelOrder
import time

import os
from .. import log


class DriverSPIBase(DriverBase):
    """Base driver for controling SPI devices on systems like the Raspberry Pi and BeagleBone"""

    def __init__(self, num, c_order=ChannelOrder.GRB, use_py_spi=True, dev="/dev/spidev0.0", SPISpeed=2):

        super(DriverSPIBase, self).__init__(num, c_order=c_order)

        self.dev = dev
        self.use_py_spi = use_py_spi
        self._spiSpeed = SPISpeed

        # File based SPI requires a bytearray so we have to overwrite _buf
        if self.use_py_spi:
            a, b = -1, -1
            d = self.dev.replace("/dev/spidev", "")
            s = d.split('.')
            if len(s) == 2:
                a = int(s[0])
                b = int(s[1])

            if a < 0 or b < 0:
                error = "When using py-spidev, the given device must be in the format /dev/spidev*.*"
                log.error(error)
                raise ValueError(error)

            self._bootstrapSPIDev()
            import spidev
            self.spi = spidev.SpiDev()
            self.spi.open(a, b)
            self.spi.max_speed_hz = int(self._spiSpeed * 1000000.0)
            log.info('py-spidev speed @ %.1f MHz',
                     (float(self.spi.max_speed_hz) / 1000000.0))
        else:
            self._buf = bytearray(self._buf)
            self.spi = open(self.dev, "wb")

    def _bootstrapSPIDev(self):
        import os.path
        import sys
        if self.use_py_spi:
            try:
                import spidev
            except:
                error = "Unable to import spidev. Please install. pip install spidev"
                log.error(error)
                raise ImportError(error)

        if not os.path.exists(self.dev):
            error = "Cannot find SPI device. Please see https://github.com/maniacallabs/bibliopixel/wiki/SPI-Setup for details."
            log.error(error)
            raise IOError(error)

        # permissions check
        try:
            open(self.dev)
        except IOError as e:
            if e.errno == 13:
                error = "Cannot find SPI device. Please see https://github.com/maniacallabs/bibliopixel/wiki/SPI-Setup for details."
                log.error(error)
                raise IOError(error)
            else:
                raise e

    def _sendData(self):
        if self.use_py_spi:
            self.spi.xfer2(self._buf)
        else:
            self.spi.write(self._buf)
            self.spi.flush()

    def update(self, data):
        self._fixData(data)
        self._sendData()
