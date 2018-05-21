from .. channel_order import ChannelOrder
from .. driver_base import DriverBase
from ... util.colors import gamma as _gamma
from . import interfaces


class SPIBase(DriverBase):
    """Base driver for controling SPI devices on systems like the Raspberry Pi
      and BeagleBone

    Provides the same parameters of
    :py:class:`bibliopixel.drivers.driver_base.DriverBase` as
    well as those below:

    :param str dev: SPI device path
    :param str spi_interface: Interface API with which to connect to the SPI
        device. One of
        :py:class:`bibliopixel.drivers.spi_interfaces.SPI_INTERFACES`
    :param int spi_speed: Output data rate, in MHz
    :param interface: DEPRECATED - Use spi_interface
    """

    def __init__(self, num, dev='/dev/spidev0.0',
                 spi_interface=None, spi_speed=1,
                 interface=None, **kwargs):
        super().__init__(num, **kwargs)
        from ...project.types.spi_interface import make
        # See https://github.com/ManiacalLabs/BiblioPixel/issues/419
        if interface:
            from ... util import deprecated
            deprecated.deprecated('SPIBase.interface')
        else:
            interface = 'FILE'

        maker = interfaces._SPI_INTERFACES[make(spi_interface or interface)]
        self._interface = maker(dev=dev, spi_speed=spi_speed)

    def _send_packet(self):
        self._interface.send_packet(self._packet)

    def _compute_packet(self):
        self._render()
        self._packet = self._interface.compute_packet(self._buf)
