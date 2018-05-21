import os
import math
from . import errors
from ... util import log
from .. spi_interfaces import SPI_INTERFACES


class SpiBaseInterface(object):
    """ abstract class for different spi backends"""

    def __init__(self, dev, spi_speed):
        self._dev = dev
        self._spi_speed = spi_speed

    def send_packet(self, data):
        """SHOULD BE PRIVATE"""
        raise NotImplementedError

    def compute_packet(self, data):
        """SHOULD BE PRIVATE"""
        return data

    def error(self, text):
        """SHOULD BE PRIVATE"""
        msg = 'Error with dev: {}, spi_speed: {} - {}'.format(
            self._dev, self._spi_speed, text)
        log.error(msg)
        raise IOError(msg)


class SpiFileInterface(SpiBaseInterface):
    """ using os open/write to send data"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not os.path.exists(self._dev):
            self.error(errors.CANT_FIND_ERROR)

        self._spi = open(self._dev, 'wb')

        log.info('file io spi dev {:s}'.format(self._dev))

    def send_packet(self, data):
        """SHOULD BE PRIVATE"""
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
            self.error(errors.CANT_FIND_ERROR)

        try:
            from periphery import SPI
            self._spi = SPI(self._dev, 0, self._spi_speed * 1e6)
        except ImportError:
            self.error(errors.CANT_IMPORT_PERIPHERY_ERROR)

        log.info('periphery spi dev {:s} speed @ {:.2f} MHz'.format(
            self._dev, self._spi.max_speed / 1e6))

    def send_packet(self, data):
        """SHOULD BE PRIVATE"""
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
            self.error(errors.BAD_FORMAT_ERROR)

        if not os.path.exists(self._dev):
            self.error(errors.CANT_FIND_ERROR)
        # permissions check
        try:
            fd = open(self._dev, 'r')
            fd.close()
        except IOError as e:
            if e.errno == 13:
                self.error(errors.PERMISSION_ERROR)
            else:
                raise e
        # import spidev and cache error
        try:
            import spidev
            self._spi = spidev.SpiDev()
        except ImportError:
            self.error(errors.CANT_IMPORT_SPIDEV_ERROR)
        self._spi.open(self._device_id, self._device_cs)
        self._spi.max_speed_hz = int(self._spi_speed * 1e6)
        log.info(
            'py-spidev dev {:s} speed @ {:.2f} MHz'.format(
                self._dev, self._spi.max_speed_hz / 1e6))

    def send_packet(self, data):
        """SHOULD BE PRIVATE"""
        self._spi.xfer2(list(data))


class SpiDummyInterface(SpiBaseInterface):
    """ interface for testing proposal"""

    def send_packet(self, data):
        """ do nothing """
        pass


_SPI_INTERFACES = [
    SpiFileInterface,
    SpiPyDevInterface,
    SpiPeripheryInterface,
    SpiDummyInterface
]
