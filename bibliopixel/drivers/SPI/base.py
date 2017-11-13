from .. channel_order import ChannelOrder
from .. driver_base import DriverBase
from ... util.colors import gamma as _gamma
from . import interfaces


class SPIBase(DriverBase):
    """Base driver for controling SPI devices on systems like the Raspberry Pi
       and BeagleBone"""
    def __init__(self, num, dev='/dev/spidev0.0',
                 spi_interface=None, spi_speed=1,
                 interface='FILE',  # DEPRECATED
                 **kwargs):
        super().__init__(num, **kwargs)
        from ...project.types.spi_interface import make
        # See https://github.com/ManiacalLabs/BiblioPixel/issues/419

        maker = interfaces._SPI_INTERFACES[make(spi_interface or interface)]
        self._interface = maker(dev=dev, spi_speed=spi_speed)

    def _send_packet(self):
        self._interface.send_packet(self._packet)

    def _compute_packet(self):
        self._render()
        self._packet = self._interface.compute_packet(self._buf)
