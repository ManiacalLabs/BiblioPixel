class Gamma(object):
    """
    Compute a fixed gamma table with 256 entries.
    """

    def __init__(self, gamma=1.0, offset=0, lower_bound=0):
        """
        :param float gamma: the root for gamma computation
        :param float offset: an offset added to the result
        :param int lower_bound: The lowest possible output value - the highest
                                is always 255.

        """
        self.gamma = gamma
        self.offset = offset
        self.lower_bound = lower_bound
        width = 255 - lower_bound

        def gam(i):
            return int(lower_bound + pow(i / 255, gamma) * width + offset)

        self.table = tuple(gam(i) for i in range(256))

    def get(self, i):
        """
        :returns: The gamma table entry
        :param int i: the index into the table
        """
        return self.table[max(0, min(255, int(i)))]


# From https://github.com/scottjgibson/PixelPi/blob/master/pixelpi.py
APA102 = Gamma(gamma=2.5, offset=0.5)
WS2801 = SM16716 = Gamma(gamma=2.5)
NONE = DEFAULT = Gamma()  # For when you need no correction

# From http://rgb-123.com/ws2812-color-output/
WS2812B = NEOPIXEL = WS2812 = Gamma(gamma=1 / 0.45)

# Color calculations from
# http://learn.adafruit.com/light-painting-with-raspberry-pi
LPD8806 = Gamma(gamma=2.5, offset=0.5, lower_bound=128)
