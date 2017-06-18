from ... import gamma
from .. channel_order import ChannelOrder
from . base import SPIBase


class APA102(SPIBase):
    """Driver for APA102 based LED strips on devices like the Raspberry Pi and BeagleBone"""

    def __init__(self, num, gamma=gamma.APA102, **kwargs):
        super().__init__(num, gamma=gamma, **kwargs)

        # APA102 requires latch bytes at the end
        self._latch_bytes = [0xFF, 0, 0, 0] * ((num // 64) + 1)

    def _compute_packet(self):
        self._render()
        # TODO: Do all this surgery in place instead
        newBuf = [0xFF] * (self.bufByteCount() + self.numLEDs)
        newBuf[1::4] = self._buf[0::3]
        newBuf[2::4] = self._buf[1::3]
        newBuf[3::4] = self._buf[2::3]
        newBuf = [0, 0, 0, 0] + newBuf
        newBuf.extend(self._latch_bytes)
        self._packet = newBuf


# This is DEPRECATED.
DriverAPA102 = APA102
