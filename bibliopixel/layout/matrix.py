import math, threading, time

from .. util import colors, deprecated, log
from . import matrix_drawing as md
from . import font
from . layout import MultiLayout
from . geometry import make_matrix_coord_map_multi
from . geometry.matrix import (
    make_matrix_coord_map, make_matrix_coord_map_positions)


ROTATION_WARNING = """
Matrix.rotation must be a multiple of 90 degrees but was in fact %s degress.
It was rounded to %s degrees."""


class Matrix(MultiLayout):
    CLONE_ATTRS = MultiLayout.CLONE_ATTRS + (
        'width', 'height', 'rotation', 'vert_flip', 'y_flip', 'serpentine',
        'pixelSize')

    def __init__(self, drivers, width=0, height=0,
                 rotation=0, vert_flip=False, y_flip=False,
                 serpentine=True,
                 threadedUpdate=False, brightness=255,
                 pixelSize=(1, 1), **kwargs):
        """Main class for matricies.

        driver --  instance that inherits from DriverBase
        width --  X axis size of matrix
        height --  Y axis size of matrix
        coord_map --  a 2D matrix defining the X,Y to strip index mapping.
            Not needed in most cases
        rotation -- how to rotate when generating the map.
            Not used if coord_map specified
        vert_flip - flips the generated map along the Y axis.
            This along with rotation can achieve any orientation
        """
        self.gen_multi = make_matrix_coord_map_multi
        super().__init__(drivers, threadedUpdate, brightness, **kwargs)

        rot_mod = rotation % 360
        self.rotation = 90 * round(rot_mod / 90)
        if self.rotation != rot_mod:
            log.warning(ROTATION_WARNING, rotation, self.rotation)

        self.width = width or getattr(self.drivers[0], 'width') or 32
        self.height = height or getattr(self.drivers[0], 'height') or 32
        self.vert_flip = vert_flip
        self.y_flip = y_flip
        self.serpentine = serpentine
        self.pixelSize = pixelSize
        pw, ph = self.pixelSize

        # If both are 0, try to assume it's a square display.
        if self.width == 0 and self.height == 0:
            square = int(math.sqrt(self.numLEDs))
            if (square * square) == self.numLEDs:
                self.width = self.height = square
            else:
                raise TypeError('No width or height passed but '
                                'the number of LEDs is not a perfect square')

        if self.width * self.height > self.numLEDs:
            raise ValueError(
                'width * height cannot exceed total pixel count! %s * %s > %s'
                % (self.width, self.height, self.numLEDs))

        if not self.coord_map:
            if len(self.drivers) == 1:
                # TODO: this should really go into documentation
                log.debug(
                    'Auto generating coordinate map. Use make_matrix_coord_map '
                    'directly if more control needed.')

                # was switched to y_flip, but need to keep vert_flip available
                y_flip = y_flip or vert_flip

                self.coord_map = make_matrix_coord_map(
                    self.width, self.height,
                    serpentine=serpentine,
                    rotation=rotation,
                    y_flip=vert_flip)

            elif self.drivers:
                raise TypeError(
                    'Must provide coord_map if using multiple drivers!')

        self.set_pixel_positions(
            make_matrix_coord_map_positions(self.coord_map))

        # If rotation is 90 or 270 degrees, dimensions need to be swapped so
        # they match the matrix rotation.
        if rotation in (90, 270):
            w = self.width
            h = self.height
            self.width = h
            self.height = w

        self.texture = None
        self.set = self._setColor

        if pw < 0 or pw > self.width or ph < 0 or ph > self.height:
            raise ValueError(
                'pixelSize must be greater than 0 '
                'and not larger than total matrix')

        if self.width % pw != 0 or self.height % ph != 0:
            raise ValueError(
                'pixelSize must evenly divide into matrix dimensions!')

        if pw == 1 and ph == 1:
            self._set = self.__setNormal
        else:
            self._set = self.__setScaled
            self.width = self.width / pw
            self.height = self.height / ph
            self.numLEDs = self.width * self.height

        self.fonts = font.fonts

    @property
    def shape(self):
        """Returns ``width, height``"""
        return self.width, self.height

    def get(self, x, y):
        """
        Return the pixel color at position (x, y), or Colors.black if that
        position is out-of-bounds.
        """
        try:
            pixel = self.coord_map[y][x]
            return self._get_base(pixel)
        except IndexError:
            return colors.Black

    def set(self, x, y, color):
        """Set the pixel color at position x, y."""
        # The actual implementation of this method is computed at construction
        # time and monkey-patched in from one of self._setTexture,
        # self.__setNormal or self.__setScaled
        raise NotImplementedError

    def get_pixel_positions(self):
        return make_matrix_coord_map_positions(self.coord_map)

    def loadFont(self, name, height, width, data):
        self.fonts[name] = {
            'data': data,
            'height': height,
            'width': width
        }

    def setTexture(self, tex=None):
        if tex is None:
            self.texture = tex
            self.set = self._setColor
            return

        if not isinstance(tex, list):
            raise ValueError('Texture must be a list!')

        if len(tex) != self.height:
            raise ValueError(
                'Given texture is must be {} high!'.format(self.height))

        for r in tex:
            if not isinstance(r, list):
                raise ValueError('Texture rows must be lists!')
            if len(r) != self.width:
                raise ValueError(
                    'Texture rows must be {} wide!'.format(self.width))

        self.texture = tex
        self.set = self._setTexture

    def __setNormal(self, x, y, color):
        try:
            pixel = self.coord_map[y][x]
            self._set_base(pixel, color)
        except IndexError:
            pass

    def __setScaled(self, x, y, color):
        sx = x * self.pixelSize[0]
        sy = y * self.pixelSize[1]

        for xs in range(sx, sx + self.pixelSize[0]):
            for ys in range(sy, sy + self.pixelSize[1]):
                self.__setNormal(xs, ys, color)

    # Set single pixel to Color value
    def _setColor(self, x, y, color=None):
        try:
            self._set(x, y, color or (0, 0, 0))
        except IndexError:
            pass

    def _setTexture(self, x, y, color=None):
        if x >= 0 and y >= 0:
            try:
                self._set(x, y, color or self.texture[y][x])
            except IndexError:
                pass

    def setHSV(self, x, y, hsv):
        color = colors.hsv2rgb(hsv)
        self._set(x, y, color)

    def setRGB(self, x, y, r, g, b):
        color = (r, g, b)
        self._set(x, y, color)

    ##########################################################################
    # Drawing Functions
    # Lovingly borrowed from Adafruit
    # https://github.com/adafruit/Adafruit-GFX-Library/blob/master/Adafruit_GFX.cpp
    ##########################################################################

    def drawCircle(self, x0, y0, r, color=None):
        """
        Draw a circle in an RGB color, with center x0, y0 and radius r.
        """
        md.draw_circle(self.set, x0, y0, r, color)

    def fillCircle(self, x0, y0, r, color=None):
        """
        Draw a filled circle in an RGB color, with center x0, y0 and radius r.
        """
        md.fill_circle(self.set, x0, y0, r, color)

    def drawLine(self, x0, y0, x1, y1, color=None, colorFunc=None, aa=False):
        """
        Draw a between x0, y0 and x1, y1 in an RGB color.

        :param colorFunc: a function that takes an integer from x0 to x1 and
            returns a color corresponding to that point
        :param aa: if True, use Bresenham's algorithm for line drawing;
            otherwise use Xiaolin Wu's algorithm
        """
        md.draw_line(self.set, x0, y0, x1, y1, color, colorFunc, aa)

    # Bresenham's algorithm
    def bresenham_line(self, x0, y0, x1, y1, color=None, colorFunc=None):
        """
        Draw line from point x0, y0 to x1, y1 using Bresenham's algorithm.

        Will draw beyond matrix bounds.
        """
        md.bresenham_line(self.set, x0, y0, x1, y1, color, colorFunc)

    # Xiaolin Wu's Line Algorithm
    def wu_line(self, x0, y0, x1, y1, color=None, colorFunc=None):
        """
        Draw a between x0, y0 and x1, y1 in an RGB color.

        :param colorFunc: a function that takes an integer from x0 to x1 and
            returns a color corresponding to that point
        :param aa: if True, use Bresenham's algorithm for line drawing;
            otherwise use Xiaolin Wu's algorithm
        """
        md.wu_line(self.set, x0, y0, x1, y1, color, colorFunc)

    def drawRect(self, x, y, w, h, color=None, aa=False):
        """
        Draw rectangle with top-left corner at x,y, width w and height h

        :param aa: if True, use Bresenham's algorithm for line drawing;
            otherwise use Xiaolin Wu's algorithm
        """
        md.draw_rect(self.set, x, y, w, h, color, aa)

    def fillRect(self, x, y, w, h, color=None, aa=False):
        """
        Draw a solid rectangle with top-left corner at (x, y), width w and
        height h.

        :param aa: if True, use Bresenham's algorithm for line drawing;
            otherwise use Xiaolin Wu's algorithm
        """
        md.fill_rect(self.set, x, y, w, h, color, aa)

    def fillScreen(self, color=None):
        """Fill the matrix with the given RGB color"""
        md.fill_rect(self.set, 0, 0, self.width, self.height, color)

    def drawRoundRect(self, x, y, w, h, r, color=None, aa=False):
        """
        Draw a rounded rectangle with top-left corner at (x, y), width w,
        height h, and corner radius r

        :param aa: if True, use Bresenham's algorithm for line drawing;
            otherwise use Xiaolin Wu's algorithm
        """
        md.draw_round_rect(self.set, x, y, w, h, r, color, aa)

    def fillRoundRect(self, x, y, w, h, r, color=None, aa=False):
        """
        Draw a rounded rectangle with top-left corner at (x, y), width w,
        height h, and corner radius r

        :param aa: if True, use Bresenham's algorithm for line drawing;
            otherwise use Xiaolin Wu's algorithm
        """
        md.fill_round_rect(self.set, x, y, w, h, r, color, aa)

    def drawTriangle(self, x0, y0, x1, y1, x2, y2, color=None, aa=False):
        """
        Draw triangle with vertices (x0, y0), (x1, y1) and (x2, y2)

        :param aa: if True, use Bresenham's algorithm for line drawing;
            Otherwise use Xiaolin Wu's algorithm
        """
        md.draw_triangle(self.set, x0, y0, x1, y1, x2, y2, color, aa)

    def fillTriangle(self, x0, y0, x1, y1, x2, y2, color=None, aa=False):
        """
        Draw filled triangle with points x0,y0 - x1,y1 - x2,y2

        :param aa: if True, use Bresenham's algorithm for line drawing;
            otherwise use Xiaolin Wu's algorithm
        """
        md.fill_triangle(self.set, x0, y0, x1, y1, x2, y2, color, aa)

    if deprecated.allowed():  # pragma: no cover
        fillTrangle = fillTriangle

    def drawChar(self, x, y, c, color, bg,
                 aa=False, font=font.default_font, font_scale=1):
        """
        Draw a single character c at at (x, y) in an RGB color.
        """
        md.draw_char(self.fonts, self.set, self.width, self.height,
                     x, y, c, color, bg, aa, font, font_scale)

    def drawText(self, text, x=0, y=0, color=None,
                 bg=colors.Off, aa=False, font=font.default_font, font_scale=1):
        """
        Draw a line of text starting at (x, y) in an RGB color.

        :param colorFunc: a function that takes an integer from x0 to x1 and
            returns a color corresponding to that point
        :param aa: if True, use Bresenham's algorithm for line drawing;
            otherwise use Xiaolin Wu's algorithm
        """
        md.draw_text(self.fonts, self.set, text, self.width, self.height,
                     x, y, color, bg, aa, font, font_scale)


if deprecated.allowed():  # pragma: no cover
    LEDMatrix = Matrix
