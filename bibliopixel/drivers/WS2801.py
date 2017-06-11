from . channel_order import ChannelOrder
from . spi_driver_base import DriverSPIBase
from .. import gamma


class WS2801(DriverSPIBase):
    """Main driver for WS2801 based LED strips on devices like the Raspberry Pi and BeagleBone"""

    def __init__(self, num, c_order=ChannelOrder.RGB,
                 spi_speed=1, gamma=gamma.WS2801, **kwargs):
        if spi_speed > 1 or spi_speed <= 0:
            raise ValueError(
                "WS2801 requires an SPI speed no greater than 1MHz or SPI speed was set <= 0")
        super().__init__(num, c_order=c_order, spi_speed=spi_speed,
                         gamma=gamma, **kwargs)


# This is DEPRECATED.
DriverWS2801 = WS2801
