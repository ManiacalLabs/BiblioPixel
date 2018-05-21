from .. channel_order import ChannelOrder
from . base import SPIBase
from ... util.colors import gamma as _gamma
from . import interfaces


MAX_PIXELS = 455


class WS281X(SPIBase):
    """
    SPI driver for WS2812(b) based LED strips on devices like
    Raspberry Pi, OrangePi, BeagleBone,..

    Provides the same parameters as
    :py:class:`bibliopixel.drivers.SPI.SPIBase`
    """

    def __init__(self, num, gamma=_gamma.WS2812, spi_speed=3.2, **kwargs):
        # WS281x need a base clock of ~1MHz - with the encoding, we need 3 times
        # this clock.  After testing 3.0 to 3.2 looks like a good value
        super().__init__(num, gamma=gamma, spi_speed=spi_speed, **kwargs)
        if isinstance(self._interface, interfaces.SpiFileInterface):
            raise ValueError('SPI File interface is unsupported by WS281X')
        if num > MAX_PIXELS:
            raise ValueError('WS2812X SPI driver only supports {} pixels max.'
                             .format(MAX_PIXELS))

    # WS2812 requires gamma correction so we run it through gamma as the
    # channels are ordered
    # As an hack to emulate PWM we use 3 bit on an SPI interface.
    # data -> spi
    # 0b0  -> 0b100
    # 0b1  -> 0b110
    def _compute_packet(self):
        # self._render()
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
