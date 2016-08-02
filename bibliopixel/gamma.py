def _table(gamma=2.5, offset=0):
    return tuple(int(pow(i / 255, gamma) * 255 + offset) for i in range(256))

# From https://github.com/scottjgibson/PixelPi/blob/master/pixelpi.py
APA102 = LPD8806 = _table(offset=0.5)
WS2801 = SM16716 = _table()

# From http://rgb-123.com/ws2812-color-output/
WS2812B = NEOPIXEL = WS2812 = _table(gamma=1 / 0.45)

# Previous constants.
# From https://github.com/scottjgibson/PixelPi/blob/master/pixelpi.py
_LPD8806 = [int(pow(float(i) / 255.0, 2.5) * 255.0 + 0.5) for i in range(256)]
_WS2801 = [int(pow(float(i) / 255.0, 2.5) * 255.0) for i in range(256)]

# From http://rgb-123.com/ws2812-color-output/
_WS2812B = [int(pow(float(i) / 255.0, 1.0 / 0.45) * 255.0) for i in range(256)]

assert tuple(_LPD8806) == LPD8806
assert tuple(_WS2801) == WS2801
assert tuple(_WS2812B) == WS2812
