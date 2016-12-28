from . driver_base import DriverBase, ChannelOrder
import time

import os
from os.path import exists
from .. import log


class SPIInterface:
    FILE = 0
    PY_SPI = 1
    PI_GPIO = 2


class DriverSPIBase(DriverBase):
    """Base driver for controling SPI devices on systems like the Raspberry Pi and BeagleBone"""

    def __init__(self, num, c_order=ChannelOrder.GRB, interface=SPIInterface.PY_SPI,
                 dev="/dev/spidev0.0", SPISpeed=2, gamma=None, open=open, exists=exists):
        super().__init__(num, c_order=c_order, gamma=gamma)

        self.open = open
        self.exists = exists
        print(self.exists)

        self.dev = dev
        self.interface = interface
        self.numSPI = -1  # ID of SPI device
        self.numCS = -1  # ID of Chip Select
        self._spiSpeed = SPISpeed

        self._bootstrapSPIDev()

        # if SpiInterface is not File we need a specific format for the python api
        if self.interface != SPIInterface.FILE and (self.numSPI < 0 or self.numCS < 0):
            error = "When using py-spidev, the given device must be in the format /dev/spidev*.*"
            log.error(error)
            raise ValueError(error)

        # File based SPI requires a bytearray so we have to overwrite _buf
        if self.interface == SPIInterface.PY_SPI:
            import spidev
            self.spi = spidev.SpiDev()
            self.spi.open(self.numSPI, self.numCS)
            self.spi.max_speed_hz = int(self._spiSpeed * 1000000.0)
            log.info('py-spidev speed @ %.1f MHz',
                     (float(self.spi.max_speed_hz) / 1000000.0))
        elif self.interface == SPIInterface.PI_GPIO:
            # @TODO support chip select http://abyz.co.uk/rpi/pigpio/python.html#spi_open
            AUX_SPI = 8
            flags = (1 << AUX_SPI)
            import pigpio
            self.pi = pigpio.pi()
            self.spi = self.pi.spi_open(self.numSPI, int(self._spiSpeed * 1000000.0), flags)
            log.info('py-spidev speed @ %.1f MHz', (float(self.spi.max_speed_hz) / 1000000.0))
        elif self.interface == SPIInterface.FILE:
            self._buf = bytearray(self._buf)
            self.spi = self.open(self.dev, "wb")
        else:
            raise ValueError('invalid interface type: "%s" not found ' % self.interface)

    def _bootstrapSPIDev(self):
        if self.interface != SPIInterface.FILE:
            self.numSPI, self.numCS = -1, -1
            d = self.dev.replace("/dev/spidev", "")
            s = d.split('.')
            if len(s) == 2:
                self.numSPI = int(s[0])
                self.numCS = int(s[1])

        if self.interface == SPIInterface.PY_SPI:
            try:
                import spidev
            except:
                error = "Unable to import spidev. Please install. pip install spidev"
                log.error(error)
                raise ImportError(error)
        elif self.interface == SPIInterface.PI_GPIO:
            try:
                import pigpio
            except:
                error = "Unable to import pigpio. Please install pigpio http://abyz.co.uk/rpi/pigpio/download.html"
                log.error(error)
                raise ImportError(error)

        if self.interface in [SPIInterface.PY_SPI, SPIInterface.FILE]:
            print(self.exists(self.dev))
            if not self.exists(self.dev):
                error = "Cannot find SPI device. Please see https://github.com/maniacallabs/bibliopixel/wiki/SPI-Setup for details."
                log.error(error)
                raise IOError(error)

            # permissions check
            try:
                self.open(self.dev)
            except IOError as e:
                if e.errno == 13:
                    error = "Cannot find SPI device. Please see https://github.com/maniacallabs/bibliopixel/wiki/SPI-Setup for details."
                    log.error(error)
                    raise IOError(error)
                else:
                    raise e

    def _send_packet(self):
        if self.interface == SPIInterface.PY_SPI:
            self.spi.xfer2(self._packet)
        elif self.interface == SPIInterface.PI_GPIO:
            self.pi.spi_write(self.spi, self._packet)
        elif self.interface == SPIInterface.FILE:
            self.spi.write(self._packet)
            self.spi.flush()

    def _compute_packet(self):
        self._render()
        self._packet = self._buf
