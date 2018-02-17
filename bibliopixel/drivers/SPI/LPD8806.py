from ... util.colors import gamma
from .. channel_order import ChannelOrder
from . base import SPIBase


class LPD8806(SPIBase):
    """Main driver for LPD8806 based LED strips on devices like the Raspberry Pi
       and BeagleBone.

    Provides the same parameters as
    :py:class:`bibliopixel.drivers.SPI.SPIBase`
    """

    def __init__(self, num, gamma=gamma.LPD8806, **kwargs):
        super().__init__(num, gamma=gamma, **kwargs)

        # LPD8806 requires latch bytes at the end
        self._latchBytes = (self.numLEDs + 31) // 32
        for i in range(0, self._latchBytes):
            self._buf.append(0)

    # LPD8806 requires gamma correction and only supports 7-bits per channel
    # running each value through gamma will fix all of this.
