class Gamma(object):
    def __init__(self, gamma=2.5, offset=0, lower_bound=0):
        self.gamma = gamma
        self.offset = offset
        self.lower_bound = lower_bound
        width = 255 - lower_bound
        gam = lambda i: int(lower_bound + pow(i / 255, gamma) * width + offset)
        self.table = tuple(gam(i) for i in range(256))


def _table(gamma=2.5, offset=0, lower_bound=0):
    width = 255 - lower_bound
    g = lambda i: lower_bound + pow(i / 255, gamma) * width + offset
    return tuple(int(g(i)) for i in range(256))


# From https://github.com/scottjgibson/PixelPi/blob/master/pixelpi.py
APA102 = _table(offset=0.5)
WS2801 = SM16716 = _table()
DEFAULT = _table(gamma=1.0)

# From http://rgb-123.com/ws2812-color-output/
WS2812B = NEOPIXEL = WS2812 = _table(gamma=1 / 0.45)

# Color calculations from
# http://learn.adafruit.com/light-painting-with-raspberry-pi
LPD8806 = _table(gamma=2.5, offset=0.5, lower_bound=128)
