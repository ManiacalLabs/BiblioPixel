def _table(gamma=2.5, offset=0, lower_bound=0):
    width = 255 - lower_bound
    g = lambda i: lower_bound + pow(i / 255, gamma) * width + offset
    return tuple(int(g(i)) for i in range(256))

# From https://github.com/scottjgibson/PixelPi/blob/master/pixelpi.py
APA102 = OLD_LPD8806 = _table(offset=0.5)
WS2801 = SM16716 = _table()

# From http://rgb-123.com/ws2812-color-output/
WS2812B = NEOPIXEL = WS2812 = _table(gamma=1 / 0.45)

# Color calculations from
# http://learn.adafruit.com/light-painting-with-raspberry-pi
NEW_LPD8806 = [0x80 | int(
    pow(float(i) / 255.0, 2.5) * 127.0 + 0.5) for i in range(256)]

NEWER_LPD8806 = _table(gamma=2.5, offset=0.5, lower_bound=128)
