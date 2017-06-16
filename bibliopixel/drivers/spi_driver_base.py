import math
import os
from . channel_order import ChannelOrder
from . driver_base import DriverBase
from .. import log


class SpiBaseInterface(object):
    """ abstract class for different spi backends"""

    def __init__(self, dev, spi_speed):
        self._dev = dev
        self._spi_speed = spi_speed

    def send_packet(self, data):
        raise NotImplementedError

    def compute_packet(self, data):
        return data


class SpiFileInterface(SpiBaseInterface):
    """ using os open/write to send data"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not os.path.exists(self._dev):
            error(CANT_FIND_ERROR)

        self._spi = open(self._dev, 'wb')

        log.info('file io spi dev {:s}'.format(self._dev))

    def send_packet(self, data):
        package_size = 4032  # bit smaller than 4096 because of headers
        for i in range(int(math.ceil(len(data) / package_size))):
            start = i * package_size
            end = (i + 1) * package_size
            self._spi.write(data[start:end])
            self._spi.flush()


class SpiPeripheryInterface(SpiBaseInterface):
    """ using `python-periphery` to send data"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not os.path.exists(self._dev):
            error(CANT_FIND_ERROR)

        try:
            from periphery import SPI
            self._spi = SPI(self._dev, 0, self._spi_speed*1e6)
        except ImportError:
            error(CANT_IMPORT_PERIPHERY_ERROR)

        log.info('periphery spi dev {:s} speed @ {:.2f} MHz'.format(self._dev, self._spi.max_speed/1e6))

    def send_packet(self, data):
        package_size = 4032  # bit smaller than 4096 because of headers
        for i in range(int(math.ceil(len(data) / package_size))):
            start = i * package_size
            end = (i + 1) * package_size
            self._spi.transfer(data[start:end])


class SpiPyDevInterface(SpiBaseInterface):
    """ using py-spidev to send data"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        d = self._dev.replace('/dev/spidev', '')
        ids = (int(i) for i in d.split('.'))
        try:
            self._device_id, self._device_cs = ids
        except:
            error(BAD_FORMAT_ERROR)

        if not os.path.exists(self._dev):
            error(CANT_FIND_ERROR)
        # permissions check
        try:
            fd = open(self._dev, 'r')
            fd.close()
        except IOError as e:
            if e.errno == 13:
                error(PERMISSION_ERROR)
            else:
                raise e
        # import spidev and cache error
        try:
            import spidev
            self._spi = spidev.SpiDev()
        except ImportError:
            error(CANT_IMPORT_SPIDEV_ERROR)
        self._spi.open(self._device_id, self._device_cs)
        self._spi.max_speed_hz = int(self._spi_speed * 1e6)
        log.info('py-spidev dev {:s} speed @ {:.2f} MHz'.format(self._dev, self._spi.max_speed_hz / 1e6))

    def send_packet(self, data):
        self._spi.xfer2(list(data))


class SpiDummyInterface(SpiBaseInterface):
    """ interface for testing proposal"""

    def send_packet(self, data):
        """ do nothing """
        pass


class DriverSPIBase(DriverBase):
    """Base driver for controling SPI devices on systems like the Raspberry Pi and BeagleBone"""

    def __init__(self, num, c_order=ChannelOrder.GRB, interface=SpiPeripheryInterface,
                 dev='/dev/spidev0.0', spi_speed=2, gamma=None):
        super().__init__(num, c_order=c_order, gamma=gamma)

        self._interface = interface(dev=dev, spi_speed=spi_speed)

    def _send_packet(self):
        self._interface.send_packet(self._packet)

    def _compute_packet(self):
        self._render()
        self._packet = self._interface.compute_packet(self._buf)


PERMISSION_ERROR = """Cannot access SPI device.
Please see

    https://github.com/maniacallabs/bibliopixel/wiki/SPI-Setup

for details.
"""

CANT_FIND_ERROR = """Cannot find SPI device.
Please see

    https://github.com/maniacallabs/bibliopixel/wiki/SPI-Setup

for details.
"""

CANT_IMPORT_PERIPHERY_ERROR = """
Unable to import periphery. Please install:
    pip install python-periphery

Please see
    https://github.com/maniacallabs/bibliopixel/wiki/SPI-Setup

for details.
"""

BAD_FORMAT_ERROR = """
When using py-spidev, `dev` must be in the format /dev/spidev*.*
"""

CANT_IMPORT_SPIDEV_ERROR = """
Unable to import spidev. Please install:

    pip install spidev
"""


def error(text):
    log.error(text)
    raise IOError(text)
