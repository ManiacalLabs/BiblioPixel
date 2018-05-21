# Original code by msurguy:
# https://github.com/ManiacalLabs/BiblioPixel/issues/51#issuecomment-228662943

import os, sys
from . channel_order import ChannelOrder
from . driver_base import DriverBase
from .. util import log
from .. colors import gamma

WS_ERROR = """
PiWS281X Requires the rpi_ws281x C extension.

Install rpi_ws281x with the following shell commands:

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

SUDO_ERROR = """
The PiWS281X driver needs to be run as sudo.  Rerun it with sudo, like this:
    sudo {command}
"""

try:
    from neopixel import Adafruit_NeoPixel, Color as NeoColor
except:
    NeoColor = None


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

STRIP_TYPES = {
    3: 0x00100800,
    4: 0x18100800,
}


# Including follow as comment as URLs in docstrings don't play well with
# sphinx
# Discussion re: running as sudo
# https://groups.google.com/d/msg/maniacal-labs-users/6hV-2_-Xmqc/wmWJK709AQAJ
# https://github.com/jgarff/rpi_ws281x/blob/master/python/neopixel.py#L106


class PiWS281X(DriverBase):
    """
    Driver for controlling WS281X LEDs via the rpi_ws281x C-extension.
    Only supported on the Raspberry Pi 2, 3, and Zero

    This driver needs to be run as sudo and requires the rpi_ws281x C extension.

    Install rpi_ws281x with the following shell commands:

        git clone https://github.com/jgarff/rpi_ws281x.git
        cd rpi_ws281x

        sudo apt-get install python-dev swig scons
        sudo scons

        cd python
        # If using default system python3
        sudo python3 setup.py build install
        # If using virtualenv, enter env then run
        python setup.py build install

    Provides the same parameters of :py:class:`.driver_base.DriverBase` as
    well as those below:

    :param int gpio: GPIO pin to output to. Typically 18 or 13
    :param int ledFreqHz: WS2812B base data frequency in Hz. Only change to
        400000 if using very old WS218B LEDs
    :param int ledDma: DMA channel to use for generating signal
                       (between 1 and 14)
    :param bool ledInvert: True to invert the signal
                       (when using NPN transistor level shift)
    """

    def __init__(
            self, num, gamma=gamma.NEOPIXEL, c_order="RGB", gpio=18,
            ledFreqHz=800000, ledDma=5, ledInvert=False,
            color_channels=3, brightness=255, **kwds):

        if not NeoColor:
            raise ValueError(WS_ERROR)
        super().__init__(num, c_order=c_order, gamma=gamma, **kwds)
        self.gamma = gamma
        if gpio not in PIN_CHANNEL.keys():
            raise ValueError('{} is not a valid gpio option!')
        try:
            strip_type = STRIP_TYPES[color_channels]
        except:
            raise ValueError('In PiWS281X, color_channels can only be 3 or 4')

        self._strip = Adafruit_NeoPixel(
            num, gpio, ledFreqHz, ledDma, ledInvert, brightness,
            PIN_CHANNEL[gpio], strip_type)
        # Intialize the library (must be called once before other functions).
        try:
            self._strip.begin()
        except RuntimeError as e:
            if os.geteuid():
                if os.path.basename(sys.argv[0]) in ('bp', 'bibliopixel'):
                    command = ['bp'] + sys.argv[1:]
                else:
                    command = ['python'] + sys.argv
                error = SUDO_ERROR.format(command=' '.join(command))
                e.args = (error,) + e.args
            raise

    def set_brightness(self, brightness):
        self._strip.setBrightness(brightness)
        return True

    def _compute_packet(self):
        self._render()
        data = self._buf
        self._packet = [tuple(data[(p * 3):(p * 3) + 3])
                        for p in range(len(data) // 3)]

    def _send_packet(self):
        for i, p in enumerate(self._packet):
            self._strip.setPixelColor(i, NeoColor(*p))

        self._strip.show()
