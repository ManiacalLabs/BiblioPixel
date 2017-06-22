import math, threading, time

from .. import colors, data_maker, font, log, matrix
from . layout import Layout
from . geometry.cube import gen_cube, pixel_positions_from_cube


class Cube(Layout):

    def __init__(self, drivers, x, y, z, coordMap=None,
                 threadedUpdate=False, brightness=255, **kwargs):
        super().__init__(drivers, threadedUpdate, brightness,
                         maker=kwargs.get('maker', data_maker.MAKER))

        self.x = x
        self.y = y
        self.z = z

        if self.x * self.y * self.z != self.numLEDs:
            raise TypeError("(x * y * z) MUST equal the total pixel count!")

        if coordMap:
            self.cube_map = coordMap
        else:
            if len(self.drivers) == 1:
                log.info('Auto generating coordinate map. Use gen_cube directly if more control needed.')
                self.cube_map = gen_cube(x, y, z)
            else:
                raise TypeError("Must provide coordMap if using multiple drivers!")

        self.set_pixel_positions(pixel_positions_from_cube(self.cube_map))

    def get_pixel_positions(self):
        return pixel_positions_from_cube(self.coord_map)

    def set(self, x, y, z, color):
        try:
            pixel = self.cube_map[z][y][x]
            self._set_base(pixel, color)
        except IndexError:
            pass

    def get(self, x, y, z):
        try:
            pixel = self.cube_map[z][y][x]
            return self._get_base(pixel)
        except IndexError:
            return 0, 0, 0

    def setHSV(self, x, y, z, hsv):
        color = colors.hsv2rgb(hsv)
        self._set(x, y, z, color)

    def setRGB(self, x, y, z, r, g, b):
        color = (r, g, b)
        self._set(x, y, z, color)


# This is DEPRECATED
LEDCube = Cube
