from . channel_order import ChannelOrder
from . spi_driver_base import DriverSPIBase


class APA102(DriverSPIBase):
    """Main driver for APA102 based LED strips on devices like the Raspberry Pi and BeagleBone"""

    def __init__(self, num, c_order=ChannelOrder.RGB, **kwargs):
        super().__init__(num, c_order=c_order, **kwargs)

        # APA102 requires latch bytes at the end
        self._latchBytes = (int(num / 64.0) + 1)

    def _render(self):
        super()._render()
        newBuf = [0xFF] * (self.bufByteCount() + self.numLEDs)
        newBuf[1::4] = self._buf[0::3]
        newBuf[2::4] = self._buf[1::3]
        newBuf[3::4] = self._buf[2::3]
        self._buf[:] = [0, 0, 0, 0] + newBuf
        self._buf.extend([0xFF, 0, 0, 0] * self._latchBytes)


# This is DEPRECATED.
DriverAPA102 = APA102
