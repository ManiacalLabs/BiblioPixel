from .. channel_order import ChannelOrder
from .. driver_base import DriverBase
from ... util.enum import resolve_enum
from . import interfaces
from enum import IntEnum
from .. ledtype import LEDTYPE
# SubDriver imports
from . APA102 import APA102
from . LPD8806 import LPD8806
from . WS281X import WS281X
from . WS2801 import WS2801


# This may look weird, but was done to keep the IDs the same
# as Serial so that ledtype can always be resolved the same
SPI_DRIVERS = {
    1: LPD8806,
    2: WS2801,
    3: WS281X,
    9: APA102
}


def SPI(ledtype=None, num=0, **kwargs):
    """Wrapper function for using SPI device drivers on systems like the Raspberry Pi and BeagleBone"""
    if ledtype is None:
        raise ValueError('Must provide ledtype value!')

    if num == 0:
        raise ValueError('Must provide num value >0!')
    ledtype = resolve_enum(LEDTYPE, ledtype)
    if ledtype not in SPI_DRIVERS.keys():
        raise ValueError('{} is not a valid LED type.'.format(type))

    return SPI_DRIVERS[ledtype](num, **kwargs)
