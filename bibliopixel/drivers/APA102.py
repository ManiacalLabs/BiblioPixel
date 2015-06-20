from spi_driver_base import *

class DriverAPA102(DriverSPIBase):
    """Main driver for APA102 based LED strips on devices like the Raspberry Pi and BeagleBone"""

    def __init__(self, num, c_order = ChannelOrder.RGB, use_py_spi = True, dev="/dev/spidev0.0", SPISpeed = 2):
        super(DriverAPA102, self).__init__(num, c_order = c_order, use_py_spi = use_py_spi, dev = dev, SPISpeed = SPISpeed)

        #APA102 requires latch bytes at the end
        self._latchBytes = (int(num/64.0)+1)

    def _fixData(self, data):
        gamma = self.gamma
        self._buf = [0 for x in range(self.bufByteCount)]
        for a, b in enumerate(self.c_order):
            self._buf[a:self.numLEDs*3:3] = [gamma[v] for v in data[b::3]]

        newBuf = [0xFF]*(self.bufByteCount+self.numLEDs)
        newBuf[1::4] = self._buf[0::3]
        newBuf[2::4] = self._buf[1::3]
        newBuf[3::4] = self._buf[2::3]
        self._buf = [0,0,0,0] + newBuf
        self._buf.extend([0xFF,0,0,0]*self._latchBytes)