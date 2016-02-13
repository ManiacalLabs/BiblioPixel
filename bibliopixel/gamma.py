# From https://github.com/scottjgibson/PixelPi/blob/master/pixelpi.py
LPD8806 = [int(pow(float(i) / 255.0, 2.5) * 255.0 + 0.5) for i in range(256)]
APA102 = LPD8806
WS2801 = [int(pow(float(i) / 255.0, 2.5) * 255.0) for i in range(256)]
SM16716 = [int(pow(float(i) / 255.0, 2.5) * 255.0) for i in range(256)]

# From http://rgb-123.com/ws2812-color-output/
WS2812B = NEOPIXEL = WS2812 = [int(pow(float(i) / 255.0, 1.0 / 0.45) * 255.0) for i in range(256)]
