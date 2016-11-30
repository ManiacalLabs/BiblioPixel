# Original code by msurguy: https://github.com/ManiacalLabs/BiblioPixel/issues/51#issuecomment-228662943
import time
from bibliopixel.drivers.driver_base import DriverBase, ChannelOrder
from .. import gamma
from .. import log
try:
    from neopixel import Adafruit_NeoPixel, Color as NeoColor
except:
    log.error('Please install rpi_ws281x: https://github.com/jgarff/rpi_ws281x/tree/master/python')
    raise


class DriverPiWS281X(DriverBase):

    def __init__(self, num, gamma=gamma.NEOPIXEL, c_order=ChannelOrder.RGB, ledPin=18, ledFreqHz=800000, ledDma=5, ledInvert=False):
        """
        num - Number of LED pixels.
        ledPin - GPIO pin connected to the pixels (must support PWM! pin 13 or 18 on RPi 3).
        ledFreqHz - LED signal frequency in hertz (800khz or 400khz)
        ledDma - DMA channel to use for generating signal (Between 1 and 14)
        ledInvert - True to invert the signal (when using NPN transistor level shift)
        """
        super(DriverPiWS281X, self).__init__(num, c_order=c_order, gamma=gamma)
        self.gamma = gamma
        self._strip = Adafruit_NeoPixel(num, ledPin, ledFreqHz, ledDma, ledInvert, 255, 0, 0x081000)
        # Intialize the library (must be called once before other functions).
        self._strip.begin()

    # WS2812 requires gamma correction so we run it through gamma as the
    # channels are ordered
    def _fixData(self, data):
        for a, b in enumerate(self.c_order):
            self._buf[a:self.numLEDs * 3:3] = [self.gamma[v] for v in data[b::3]]

    # Set Brightness of the strip. A brightness of 0 is the darkest and 255 is
    # the brightest
    def setMasterBrightness(self, brightness):
        self._strip.setBrightness(brightness)

    # Push new data
    def update(self, data):
        # handle channel order and gamma correction
        self._fixData(data)

        pixels = [tuple(data[(p * 3):(p * 3) + 3])
                  for p in range(len(data) / 3)]

        for i in range(len(data) / 3):
            self._strip.setPixelColor(i, NeoColor(pixels[i][0], pixels[i][1], pixels[i][2]))

        self._strip.show()


MANIFEST = [
    {
        "id": "WS2801",
        "class": DriverPiWS281X,
        "type": "driver",
        "display": "WS281X",
        "desc": "Interface with WS281X (WS2811, WS2812, WS2812b) on the Raspberry Pi. Requires install of rpi_ws281x",
        "params": [{
                "id": "num",
                "label": "# Pixels",
                "type": "int",
                "default": 1,
                "min": 1,
                "help": "Total pixels in display."
        }, {
            "id": "c_order",
            "label": "Channel Order",
            "type": "combo",
            "options": {
                    0: "RGB",
                    1: "RBG",
                    2: "GRB",
                    3: "GBR",
                    4: "BRG",
                    5: "BGR"
            },
            "options_map": [
                [0, 1, 2],
                [0, 2, 1],
                [1, 0, 2],
                [1, 2, 0],
                [2, 0, 1],
                [2, 1, 0]
            ],
            "default": 0
        }, {
            "id": "ledPin",
            "label": "LED Pin",
            "help": "LED GPIO pin on Raspberry Pi",
            "type": "int",
            "default": 18,
        }]
    }
]
