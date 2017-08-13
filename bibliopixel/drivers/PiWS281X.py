# Original code by msurguy: https://github.com/ManiacalLabs/BiblioPixel/issues/51#issuecomment-228662943

from . channel_order import ChannelOrder
from . driver_base import DriverBase
from .. util import log
from .. colors import gamma

try:
    from neopixel import Adafruit_NeoPixel, Color as NeoColor
except:
    WS_ERROR = """PiWS281X Requires the rpi_ws281x C extension.
Install rpi_ws281x with below commands:
git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
sudo apt-get install python-dev swig scons
sudo scons
cd python
# If using default system python3
sudo python3 setup.py build install
# If using virtualenv, enter env then run
python setup.py build install
    """
    log.error(WS_ERROR)
    raise


PIN_CHANNEL = {
    12: 0,
    18: 0,
    40: 0,
    52: 0,
    13: 1,
    19: 1,
    41: 1,
    45: 1,
    53: 1,
    10: 0,  # Technically SPI
}


class PiWS281X(DriverBase):
    """
    Driver for controlling WS281X LEDs via the rpi_ws281x C-extension.
    Only supported on the Raspberry Pi 2 & 3
    """
    def __init__(self, num, gamma=gamma.NEOPIXEL, c_order=ChannelOrder.RGB, gpio=18,
                 ledFreqHz=800000, ledDma=5, ledInvert=False, **kwds):
        """
        num - Number of LED pixels.
        gpio - GPIO pin connected to the pixels (must support PWM! GPIO 13 or 18 (pins 33 or 12) on RPi 3).
        ledFreqHz - LED signal frequency in hertz (800khz or 400khz)
        ledDma - DMA channel to use for generating signal (Between 1 and 14)
        ledInvert - True to invert the signal (when using NPN transistor level shift)
        """
        super().__init__(num, c_order=c_order, gamma=gamma, **kwds)
        self.gamma = gamma
        if gpio not in PIN_CHANNEL.keys():
            raise ValueError('{} is not a valid gpio option!')
        self._strip = Adafruit_NeoPixel(num, gpio, ledFreqHz,
                                        ledDma, ledInvert, 255, PIN_CHANNEL[gpio], 0x081000)
        # Intialize the library (must be called once before other functions).
        self._strip.begin()

    def set_brightness(self, brightness):
        self._strip.setBrightness(brightness)
        return True

    def _compute_packet(self):
        self._render()
        data = self._buf
        self._packet = [tuple(data[(p * 3):(p * 3) + 3]) for p in range(len(data) // 3)]

    def _send_packet(self):
        for i, p in enumerate(self._packet):
            self._strip.setPixelColor(i, NeoColor(*p))

        self._strip.show()
