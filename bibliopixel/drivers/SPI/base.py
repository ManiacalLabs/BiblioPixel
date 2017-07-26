from .. channel_order import ChannelOrder
from .. driver_base import DriverBase
from ... colors import gamma as _gamma
from ... util.enum import resolve_enum
from . import interfaces


class SPIBase(DriverBase):
    """Base driver for controling SPI devices on systems like the Raspberry Pi and BeagleBone"""
    def __init__(self, num, dev='/dev/spidev0.0',
                 interface='FILE', spi_speed=1,
                 **kwargs):

        super().__init__(num, **kwargs)

        iface = resolve_enum(interfaces.SPI_INTERFACES, interface)
        if iface >= len(interfaces._SPI_INTERFACES):
            raise ValueError('{} is not a valid interface.'.format(interface))

        self._interface = interfaces._SPI_INTERFACES[iface](dev=dev, spi_speed=spi_speed)

    def _send_packet(self):
        self._interface.send_packet(self._packet)

    def _compute_packet(self):
        self._render()
        self._packet = self._interface.compute_packet(self._buf)
