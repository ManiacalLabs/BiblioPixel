def _table(gamma=2.5, offset=0):
    return tuple(int(pow(i / 255, gamma) * 255 + offset) for i in range(256))

# From https://github.com/scottjgibson/PixelPi/blob/master/pixelpi.py
APA102 = LPD8806 = _table(offset=0.5)
WS2801 = SM16716 = _table()

# From http://rgb-123.com/ws2812-color-output/
WS2812B = NEOPIXEL = WS2812 = _table(gamma=1 / 0.45)
