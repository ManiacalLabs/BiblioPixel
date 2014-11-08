from spi_driver_base import *
import os
os.sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
import gamma

class DriverWS2801(DriverSPIBase):
    """Main driver for WS2801 based LED strips on devices like the Raspberry Pi and BeagleBone"""
    
    def __init__(self, num, c_order = ChannelOrder.RGB, use_py_spi = True, dev="/dev/spidev0.0", SPISpeed = 1):
        if SPISpeed > 1 or SPISpeed <= 0:
            raise ValueError("WS2801 requires an SPI speed no greater than 1MHz or SPI speed was set <= 0")
        super(DriverWS2801, self).__init__(num, c_order = c_order, use_py_spi = use_py_spi, dev = dev, SPISpeed = SPISpeed)
           
        self.gamma = gamma.WS2801

    #WS2801 requires gamma correction so we run it through gamma as the channels are ordered
    def _fixData(self, data):
        for a, b in enumerate(self.c_order):
            self._buf[a:self.numLEDs*3:3] = [self.gamma[v] for v in data[b::3]]

