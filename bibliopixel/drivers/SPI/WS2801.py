from .. channel_order import ChannelOrder
from . base import SPIBase
from ... colors import gamma


class WS2801(SPIBase):
    """Main driver for WS2801 based LED strips on devices like the Raspberry Pi and BeagleBone"""

    def __init__(self, num, gamma=gamma.WS2801, spi_speed=1, **kwargs):
        if not (0 < spi_speed <= 1):
            raise ValueError(
                'WS2801 requires an SPI speed of 1MHz but was set to {}MHz'.format(spi_speed))
        super().__init__(num, gamma=gamma, spi_speed=spi_speed, **kwargs)
