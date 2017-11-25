from .. import colors
from . layout import Layout
from . geometry.strip import make_strip_coord_map_positions


class Strip(Layout):

    def __init__(self, drivers, threadedUpdate=False,
                 brightness=255, pixelWidth=1, coord_map=None, **kwargs):
        super().__init__(drivers, threadedUpdate, brightness, **kwargs)

        self.pixelWidth = pixelWidth
        if self.pixelWidth < 1 or self.pixelWidth > self.numLEDs:
            raise ValueError(
                "pixelWidth must be greater than 0 and less than or equal to the total LED count!")
        if self.numLEDs % self.pixelWidth != 0:
            raise ValueError(
                "Total LED count must be evenly divisible by pixelWidth!")
        if self.pixelWidth == 1:
            self.set = self._set
        else:
            self.set = self._setScaled
            self.num_pixels = int(self.numLEDs / self.pixelWidth)

        self.coord_map = coord_map
        if self.coord_map:
            if len(self.coord_map) != self.numLEDs:
                raise ValueError('coord_map length must equal total number of pixels!')
            self.set_base = self._set_strip_mapped
        else:
            self.set_base = self._set_base

        self.set_pixel_positions(make_strip_coord_map_positions(self.numLEDs))

    def get(self, pixel):
        """Get RGB color tuple of color at index pixel"""
        return self._get_base(pixel * self.pixelWidth)

    def _set_strip_mapped(self, pixel, color):
        if pixel >= 0 and pixel < self.numLEDs:
            pixel = self.coord_map[pixel]
            self._set_base(pixel, color)

    # Set single pixel to Color value
    def _set(self, pixel, color):
        """Set pixel to RGB color tuple"""
        self.set_base(pixel, color)

    def _setScaled(self, pixel, color):
        start = pixel * self.pixelWidth
        for p in range(start, start + self.pixelWidth):
            self.set_base(p, color)

    def get(self, pixel):
        """Get RGB color tuple of color at index pixel"""
        return self._get_base(pixel)

    # Set single pixel to RGB value
    def setRGB(self, pixel, r, g, b):
        """Set single pixel using individual RGB values instead of tuple"""
        self.set(pixel, (r, g, b))

    def setHSV(self, pixel, hsv):
        """Set single pixel to HSV tuple"""
        color = colors.hsv2rgb(hsv)
        self.set(pixel, color)

    # turns off the desired pixel
    def setOff(self, pixel):
        """Set single pixel off"""
        self.set(pixel, (0, 0, 0))


# This is DEPRECATED
LEDStrip = Strip
