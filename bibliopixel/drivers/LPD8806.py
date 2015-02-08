from spi_driver_base import *

class DriverLPD8806(DriverSPIBase):
    """Main driver for LPD8806 based LED strips on devices like the Raspberry Pi and BeagleBone"""
    
    def __init__(self, num, c_order = ChannelOrder.RGB, use_py_spi = True, dev="/dev/spidev0.0", SPISpeed = 2):
        super(DriverLPD8806, self).__init__(num, c_order = c_order, use_py_spi = use_py_spi, dev = dev, SPISpeed = SPISpeed)
           
        # Color calculations from
        # http://learn.adafruit.com/light-painting-with-raspberry-pi
        self.gamma = [0x80 | int(pow(float(i) / 255.0, 2.5) * 127.0 + 0.5) for i in range(256)]

        #LPD8806 requires latch bytes at the end
        self._latchBytes = (self.numLEDs + 31) / 32
        for i in range(0, self._latchBytes):
            self._buf.append(0)

    #LPD8806 requires gamma correction and only supports 7-bits per channel
    #running each value through gamma will fix all of this.
    #def _fixData(self, data):
    #    for a, b in enumerate(self.c_order):
    #        self._buf[a:self.numLEDs*3:3] = [self.gamma[v] for v in data[b::3]]


