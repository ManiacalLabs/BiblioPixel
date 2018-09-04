import math, threading, time

from .. util import colors, log
from . import font
from . layout import Layout
from . geometry.cube import make_cube_coord_map, make_cube_coord_map_positions


class Cube(Layout):
    CLONE_ATTRS = Layout.CLONE_ATTRS + ('x', 'y', 'z')

    def __init__(self, drivers, x, y, z, coord_map=None,
                 threadedUpdate=False, brightness=255, **kwargs):
        super().__init__(drivers, threadedUpdate, brightness, **kwargs)
        self.x = x
        self.y = y
        self.z = z

        if self.x * self.y * self.z != self.numLEDs:
            raise TypeError("(x * y * z) MUST equal the total pixel count!")

        if coord_map:
            self.coord_map = coord_map
        else:
            if len(self.drivers) == 1:
                self.coord_map = make_cube_coord_map(x, y, z)
            else:
                raise TypeError(
                    "Must provide coord_map if using multiple drivers!")

        self.set_pixel_positions(make_cube_coord_map_positions(self.coord_map))

    def get_pixel_positions(self):
        return make_cube_coord_map_positions(self.coord_map)

    @property
    def shape(self):
        """Returns ``x, y, z``"""
        return self.x, self.y, self.z

    def set(self, x, y, z, color):
        try:
            pixel = self.coord_map[z][y][x]
            self._set_base(pixel, color)
        except IndexError:
            pass

    def get(self, x, y, z):
        try:
            pixel = self.coord_map[z][y][x]
            return self._get_base(pixel)
        except IndexError:
            return 0, 0, 0

    def setHSV(self, x, y, z, hsv):
        color = colors.hsv2rgb(hsv)
        self._set(x, y, z, color)

    def setRGB(self, x, y, z, r, g, b):
        color = (r, g, b)
        self._set(x, y, z, color)


from .. util import deprecated
if deprecated.allowed():  # pragma: no cover
    LEDCube = Cube
