import math, threading, time

from .. import colors, font, matrix, timedata, update_thread

from . base import LEDBase


class MatrixRotation:
    ROTATE_0 = 0  # no rotation
    ROTATE_90 = 3  # rotate 90 degrees
    ROTATE_180 = 2  # rotate 180 degrees
    ROTATE_270 = 1  # rotate 270 degrees


def mapGen(width, height, serpentine=True, offset=0, rotation=MatrixRotation.ROTATE_0, vert_flip=False):
    """Helper method to generate X,Y coordinate maps for strips"""

    result = []
    for y in range(height):
        if not serpentine or y % 2 == 0:
            result.append([(width * y) + x + offset for x in range(width)])
        else:
            result.append([((width * (y + 1)) - 1) - x +
                           offset for x in range(width)])

    for i in range(rotation):
        result = list(zip(*result[::-1]))

    if vert_flip:
        result = result[::-1]

    return result


class MultiMapBuilder():

    def __init__(self):
        self.map = []
        self.offset = 0

    def addRow(self, *maps):
        yOff = len(self.map)
        lengths = [len(m) for m in maps]
        h = max(lengths)
        if(min(lengths) != h):
            raise ValueError("All maps in row must be the same height!")

        offsets = [0 + self.offset]
        count = 0
        for m in maps:
            offsets.append(h * len(m[0]) + offsets[count])
            count += 1

        for y in range(h):
            self.map.append([])
            for x in range(len(maps)):
                self.map[y + yOff] += [i + offsets[x] for i in maps[x][y]]

        self.offset = offsets[len(offsets) - 1]


class LEDMatrix(LEDBase):

    def __init__(self, drivers, width=0, height=0, coordMap=None, rotation=MatrixRotation.ROTATE_0, vert_flip=False, serpentine=True, threadedUpdate=False, masterBrightness=255, pixelSize=(1, 1)):
        """Main class for matricies.
        driver - instance that inherits from DriverBase
        width - X axis size of matrix
        height - Y axis size of matrix
        coordMap - a 2D matrix defining the X,Y to strip index mapping. Not needed in most cases
        rotation - how to rotate when generating the map. Not used if coordMap specified
        vert_flip - flips the generated map along the Y axis. This along with rotation can achieve any orientation
        """
        super().__init__(drivers, threadedUpdate, masterBrightness)

        if width == 0 and height == 0:
            if len(self.driver) != 1:
                raise TypeError(
                    "Must provide width and height if using multiple drivers!")
            width = self.driver[0].width
            height = self.driver[0].height

        self.width = width
        self.height = height
        self.pixelSize = pixelSize
        pw, ph = self.pixelSize

        # if both are 0 try to assume it's a square display
        if self.width == 0 and self.height == 0:
            square = int(math.sqrt(self.numLEDs))
            if (square * square) == self.numLEDs:
                self.width = self.height = square
            else:
                raise TypeError(
                    "No width or height passed but the number of LEDs is not a perfect square")

        if self.width * self.height != self.numLEDs:
            raise TypeError("width * height MUST equal the total pixel count!")

        if coordMap:
            self.matrix_map = coordMap
        else:
            if len(self.drivers) == 1:
                self.matrix_map = mapGen(self.width, self.height, serpentine)
            else:
                raise TypeError(
                    "Must provide coordMap if using multiple drivers!")

        # apply rotation
        for i in range(rotation):
            self.matrix_map = list(zip(*self.matrix_map[::-1]))

        # apply flip
        if vert_flip:
            self.matrix_map = self.matrix_map[::-1]

        # if 90 or 270 rotation dimensions need to be swapped so they match the
        # matrix rotation
        if rotation % 2 != 0:
            w = self.width
            h = self.height
            self.width = h
            self.height = w

        self.texture = None
        self.set = self._setColor

        if pw < 0 or pw > self.width or ph < 0 or ph > self.height:
            raise ValueError(
                "pixelSize must be greater than 0 and not larger than total matrix!")
        if self.width % pw != 0 or self.height % ph != 0:
            raise ValueError(
                "pixelSize must evenly divide into matrix dimensions!")

        if pw == 1 and ph == 1:
            self._set = self.__setNormal
        else:
            self._set = self.__setScaled
            self.width = self.width / pw
            self.height = self.height / ph
            self.numLEDs = self.width * self.height

        self.fonts = font.fonts

    def loadFont(self, name, height, width, data):
        self.fonts[name] = {
            "data": data,
            "height": height,
            "width": width
        }

    def setTexture(self, tex=None):
        if tex is None:
            self.texture = tex
            self.set = self._setColor
        else:
            if not isinstance(tex, list):
                raise ValueError("Texture must be a list!")
            elif len(tex) != self.height:
                raise ValueError(
                    "Given texture is must be {} high!".format(self.height))
            else:
                for r in tex:
                    if not isinstance(r, list):
                        raise ValueError("Texture rows must be lists!")
                    elif len(r) != self.width:
                        raise ValueError(
                            "Texture rows must be {} wide!".format(self.width))

            self.texture = tex
            self.set = self._setTexture

    def __setNormal(self, x, y, color):
        try:
            pixel = self.matrix_map[y][x]
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

    def get(self, x, y):
        try:
            pixel = self.matrix_map[y][x]
            return self._get_base(pixel)
        except IndexError:
            return 0, 0, 0

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
        """Draws a circle at point x0, y0 with radius r of the specified RGB color"""
        matrix.draw_circle(self.set, x0, y0, r, color)

    def fillCircle(self, x0, y0, r, color=None):
        """Draws a filled circle at point x0,y0 with radius r and specified color"""
        matrix.fill_circle(self.set, x0, y0, r, color)

    def drawLine(self, x0, y0, x1, y1, color=None, colorFunc=None, aa=False):
        matrix.draw_line(self.set, x0, y0, x1, y1, color, colorFunc, aa)

    # Bresenham's algorithm
    def bresenham_line(self, x0, y0, x1, y1, color=None, colorFunc=None):
        """Draw line from point x0,y0 to x,1,y1. Will draw beyond matrix bounds."""
        matrix.bresenham_line(self.set, x0, y0, x1, y1, color, colorFunc)

    # Xiaolin Wu's Line Algorithm
    def wu_line(self, x0, y0, x1, y1, color=None, colorFunc=None):
        matrix.wu_line(self.set, x0, y0, x1, y1, color, colorFunc)

    def drawRect(self, x, y, w, h, color=None, aa=False):
        """Draw rectangle with top-left corner at x,y, width w and height h"""
        matrix.draw_rect(self.set, x, y, w, h, color, aa)

    def fillRect(self, x, y, w, h, color=None, aa=False):
        """Draw solid rectangle with top-left corner at x,y, width w and height h"""
        matrix.fill_rect(self.set, x, y, w, h, color, aa)

    def fillScreen(self, color=None):
        """Fill the matrix with the given RGB color"""
        matrix.fill_rect(self.set, 0, 0, self.width, self.height, color)

    def drawRoundRect(self, x, y, w, h, r, color=None, aa=False):
        """Draw rectangle with top-left corner at x,y, width w, height h, and corner radius r"""
        matrix.draw_round_rect(self.set, x, y, w, h, r, color, aa)

    def fillRoundRect(self, x, y, w, h, r, color=None, aa=False):
        """Draw solid rectangle with top-left corner at x,y, width w, height h, and corner radius r"""
        matrix.fill_round_rect(self.set, x, y, w, h, r, color, aa)

    def drawTriangle(self, x0, y0, x1, y1, x2, y2, color=None, aa=False):
        """Draw triangle with points x0,y0 - x1,y1 - x2,y2"""
        matrix.draw_triangle(self.set, x0, y0, x1, y1, x2, y2, color, aa)

    def fillTriangle(self, x0, y0, x1, y1, x2, y2, color=None, aa=False):
        """Draw solid triangle with points x0,y0 - x1,y1 - x2,y2"""
        matrix.fill_triangle(self.set, x0, y0, x1, y1, x2, y2, color, aa)

    fillTrangle = fillTriangle  # DEPRECATED!

    def drawChar(self, x, y, c, color, bg, aa=False, font=font.default_font, font_scale=1):
        matrix.draw_char(self.fonts, self.set, self.width, self.height,
                         x, y, c, color, bg, aa, font, font_scale)

    def drawText(self, text, x=0, y=0, color=None, bg=colors.Off, aa=False, font=font.default_font, font_scale=1):
        matrix.draw_text(self.fonts, self.set, text, self.width, self.height,
                         x, y, color, bg, aa, font, font_scale)


# Takes a matrix and displays it as individual columns over time
class LEDPOV(LEDMatrix):

    def __init__(self, drivers, povHeight, width, rotation=MatrixRotation.ROTATE_0, vert_flip=False, threadedUpdate=False, masterBrightness=255):
        self.numLEDs = povHeight * width

        super().__init__(drivers, width, povHeight, None,
                         rotation, vert_flip, threadedUpdate, masterBrightness)

    # This is the magic. Overriding the normal push_to_driver() method
    # It will automatically break up the frame into columns spread over
    # frameTime (ms)
    def push_to_driver(self, frameTime=None):
        if frameTime:
            self._frameTotalTime = frameTime

        sleep = None
        if self._frameTotalTime:
            sleep = (self._frameTotalTime - self._frameGenTime) / self.width

        width = self.width
        for h in range(width):
            start = time.time() * 1000.0

            def color(i):
                return self._colors[(h + width * i) * 3]
            # TODO: Figure out what line below needs to do
            # buf = [color(i) for i in range(self.height)]
            self.drivers[0].update_colors()
            sendTime = (time.time() * 1000.0) - start
            if sleep:
                time.sleep(max(0, (sleep - sendTime) / 1000.0))


class LEDCircle(LEDBase):

    def __init__(self, drivers, rings, maxAngleDiff=0, rotation=0, threadedUpdate=False, masterBrightness=255):
        super().__init__(drivers, threadedUpdate, masterBrightness)
        self.rings = rings
        self.maxAngleDiff = maxAngleDiff
        self._full_coords = False
        for r in self.rings:
            self._full_coords |= (len(r) > 2)
        self.ringCount = len(self.rings)
        self.lastRing = self.ringCount - 1
        self.ringSteps = []
        num = 0
        for r in self.rings:
            if self._full_coords:
                count = len(r)
            else:
                count = (r[1] - r[0] + 1)
            self.ringSteps.append(360.0 / count)
            num += count

        self.rotation = rotation

        if self.numLEDs != num:
            raise ValueError(
                "Total ring LED count does not equal driver LED count!")

    def __genOffsetFromAngle(self, angle, ring):
        if ring >= self.ringCount:
            return -1

        angle = (angle + self.rotation) % 360
        offset = int(round(angle / self.ringSteps[ring]))

        # wraps it back around
        if self._full_coords:
            length = len(self.rings[ring]) - 1
        else:
            length = self.rings[ring][1] - self.rings[ring][0]

        if offset > length:
            offset = 0

        if self.maxAngleDiff > 0:
            calcAngle = (offset * self.ringSteps[ring]) % 360
            diff = abs(angle - calcAngle)
            if diff > self.maxAngleDiff:
                return -1

        return offset

    def angleToPixel(self, angle, ring):
        offset = self.__genOffsetFromAngle(angle, ring)
        if offset < 0:
            return offset

        if self._full_coords:
            return self.rings[ring][offset]
        else:
            return self.rings[ring][0] + offset

    # Set single pixel to Color value
    def set(self, ring, angle, color):
        """Set pixel to RGB color tuple"""
        pixel = self.angleToPixel(angle, ring)
        self._set_base(pixel, color)

    def get(self, ring, angle):
        """Get RGB color tuple of color at index pixel"""
        pixel = self.angleToPixel(angle, ring)
        return self._get_base(pixel)

    def drawRadius(self, angle, color, startRing=0, endRing=-1):
        if startRing < 0:
            startRing = 0
        if endRing < 0 or endRing > self.lastRing:
            endRing = self.lastRing
        for ring in range(startRing, endRing + 1):
            self.set(ring, angle, color)

    def fillRing(self, ring, color, startAngle=0, endAngle=None):
        if endAngle is None:
            endAngle = 359

        if ring >= self.ringCount:
            raise ValueError("Invalid ring!")

        def pixelRange(ring, start=0, stop=-1):
            r = self.rings[ring]
            if stop == -1:
                if self._full_coords:
                    stop = len(r) - 1
                else:
                    stop = r[1] - r[0]

            if self._full_coords:
                return [r[i] for i in range(start, stop + 1)]
            else:
                return range(start + r[0], stop + r[0] + 1)

        start = self.__genOffsetFromAngle(startAngle, ring)
        end = self.__genOffsetFromAngle(endAngle, ring)

        pixels = []
        if start >= end:
            pixels = pixelRange(ring, start)
            pixels.extend(pixelRange(ring, 0, end))
        elif start == end and startAngle > endAngle:
            pixels = pixelRange(ring)
        else:
            pixels = pixelRange(ring, start, end)

        for i in pixels:
            self._set_base(i, color)
