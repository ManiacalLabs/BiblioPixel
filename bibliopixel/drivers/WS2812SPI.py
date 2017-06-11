from . spi_driver_base import DriverSPIBase, ChannelOrder
from .. import gamma as _gamma
from .. import log


class WS281XSPI(DriverSPIBase):
    """
    SPI driver for WS2812(b) based LED strips on devices like
    Raspberry Pi, OrangePi, BeagleBone,..
    """

    def __init__(self, num, **kwargs):
        # WS281x need a base clock of ~1MHz with the encoding we need 3 times this clock
        # After testing 3.2 looks like a good value
        spi_speed = 3.2
        super().__init__(num, c_order=ChannelOrder.GRB, spi_speed=spi_speed,
                         gamma=_gamma.WS2812, **kwargs)

    # WS2812 requires gamma correction so we run it through gamma as the
    # channels are ordered
    # As an hack to emulate PWM we use 3 bit on an SPI interface.
    # data -> spi
    # 0b0  -> 0b100
    # 0b1  -> 0b110
    def _compute_packet(self):
        super()._compute_packet()

        # buffer for result
        # [0] fixes, first led show green when should be off
        buf2 = bytearray([0])
        for byte in self._buf:
            # save each byte in an int var
            tmp = 0
            for i in range(8):
                tmp |= (0b100 | (0b10 if (byte & 1 << i) > 0 else 0)) << (i * 3)
            # save each byte in little endian
            buf2.append(tmp >> 16 & 0xff)
            buf2.append(tmp >> 8 & 0xff)
            buf2.append(tmp & 0xff)

        self._packet = buf2


MANIFEST = [
    {
        "id": "WS2812SPI",
        "class": WS281XSPI,
        "type": "driver",
        "display": "WS2812 (SPI)",
        "desc": "Interface with WS2812 / WS2812B strips over a native SPI port (Pi, BeagleBone, etc.)",
        "params": [{
            "id": "num",
            "label": "# Pixels",
            "type": "int",
            "default": 1,
            "min": 1,
            "max": 455,
            "help": "Total pixels in display."
        }]
    }
]
