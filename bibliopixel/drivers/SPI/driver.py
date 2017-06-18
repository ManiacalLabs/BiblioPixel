from .. channel_order import ChannelOrder
from .. driver_base import DriverBase
from ... util.enum import resolve_enum
from . import interfaces
from enum import IntEnum
# SubDriver imports
from . APA102 import APA102
from . LPD8806 import LPD8806
from . WS281X import WS281XSPI
from . WS2801 import WS2801


class SPI_LEDTYPE(IntEnum):
    APA102 = 0
    DOTSTAR = 0
    WS2801 = 1
    WS281X = 2
    WS2812 = 2
    WS2812B = 2
    NEOPIXEL = 2
    LPD8806 = 3


SPI_DRIVERS = [
    APA102,
    WS2801,
    WS281XSPI,
    LPD8806
]


class SPI(DriverBase):
    """Driver for controling SPI devices on systems like the Raspberry Pi and BeagleBone"""
    # This is little more than a metaclass at this point.
    # Simply returning the actual desired SPI class

    def __new__(self, type, num, **kwargs):
        ledtype = resolve_enum(SPI_LEDTYPE, type)
        if ledtype >= len(SPI_DRIVERS):
            raise ValueError('{} is not a valid LED type.'.format(type))

        return SPI_DRIVERS[ledtype](num, **kwargs)
