import math, threading, time

from .. import colors, data_maker, font, matrix
from . base import LEDBase
from . multimap import MatrixRotation, mapGen, MultiMapBuilder
from . coord_map import gen_cube, point_list_from_cube


class LEDCube(LEDBase):

    def __init__(self, drivers, x, y, z, coordMap=None, threadedUpdate=False, masterBrightness=255, maker=data_maker.MAKER):
        super().__init__(drivers, threadedUpdate, masterBrightness, maker)

        self.x = x
        self.y = y
        self.z = z

        # self.pixelSize = pixelSize
        # pw, ph = self.pixelSize

        if self.x * self.y * self.z != self.numLEDs:
            raise TypeError("(x * y * z) MUST equal the total pixel count!")

        if coordMap:
            self.cube_map = coordMap
        # else:
        #     if len(self.drivers) == 1:
        #         self.cube_map = mapGen(self.width, self.height, serpentine)
        #     else:
        #         raise TypeError(
        #             "Must provide coordMap if using multiple drivers!")

        self.set_point_list(point_list_from_cube(self.cube_map))

        self.texture = None
        self.set = self._setColor
        self._set = self.__setNormal

        # if pw < 0 or pw > self.width or ph < 0 or ph > self.height:
        #     raise ValueError(
        #         "pixelSize must be greater than 0 and not larger than total matrix!")
        # if self.width % pw != 0 or self.height % ph != 0:
        #     raise ValueError(
        #         "pixelSize must evenly divide into matrix dimensions!")

        # if pw == 1 and ph == 1:
        #     self._set = self.__setNormal
        # else:
        #     self._set = self.__setScaled
        #     self.width = self.width / pw
        #     self.height = self.height / ph
        #     self.numLEDs = self.width * self.height

    def get_point_list(self):
        return point_list_from_cube(self.coord_map)

    def __setNormal(self, x, y, z, color):
        try:
            pixel = self.cube_map[z][y][x]
            self._set_base(pixel, color)
        except IndexError:
            pass

    # def __setScaled(self, x, y, color):
    #     sx = x * self.pixelSize[0]
    #     sy = y * self.pixelSize[1]
    #
    #     for xs in range(sx, sx + self.pixelSize[0]):
    #         for ys in range(sy, sy + self.pixelSize[1]):
    #             self.__setNormal(xs, ys, color)

    # Set single pixel to Color value
    def _setColor(self, x, y, z, color=None):
        try:
            self._set(x, y, z, color or (0, 0, 0))
        except IndexError:
            pass

    # def _setTexture(self, x, y, color=None):
    #     if x >= 0 and y >= 0:
    #         try:
    #             self._set(x, y, color or self.texture[y][x])
    #         except IndexError:
    #             pass

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
