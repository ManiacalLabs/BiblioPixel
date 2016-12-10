import math
import threading
import time

from . import colors, font, matrix, timedata, update_thread


class LEDBase(object):

    def __init__(self, drivers, threadedUpdate, masterBrightness):
        """Base LED class. Use LEDStrip or LEDMatrix instead!"""
        self.drivers = drivers if isinstance(drivers, list) else [drivers]

        if not hasattr(self, 'numLEDs'):
            self.numLEDs = sum(d.numLEDs for d in self.drivers)

        # This buffer will always be the same list - i.e. is guaranteed to only
        # be changed by list surgery, never assignment.
        self._colors = timedata.ColorList255()
        self.all_off()
        assert len(self._colors) == self.numLEDs

        pos = 0
        for d in self.drivers:
            d.set_colors(self._colors, pos)
            pos += d.numLEDs

        self.masterBrightness = 255

        self._frameGenTime = 0
        self._frameTotalTime = None

        self._threadedUpdate = threadedUpdate

        if self._threadedUpdate:
            self._updateThread = update_thread.UpdateThread(self.drivers)
            self._updateThread.start()

        self._waitingBrightness = False
        self._waitingBrightnessValue = None
        self._threadedAnim = False

        self.set_brightness(masterBrightness)

    def update(self):
        """DEPRECATED - use self.push_to_driver()"""
        return self.push_to_driver()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return self.cleanup()

    def cleanup(self):
        pass

    def _get_base(self, pixel):
        if pixel >= 0 and pixel < self.numLEDs:
            return self._colors[pixel]
        return 0, 0, 0  # don't go out of bounds

    def _set_base(self, pixel, color):
        if pixel >= 0 and pixel < self.numLEDs:
            if self.masterBrightness < 255:
                color = ((c * self.masterBrightness) >> 8 for c in color)
            self._colors[pixel] = tuple(color)

    def waitForUpdate(self):
        if self._threadedUpdate:
            while all([d._thread.sending() for d in self.drivers]):
                time.sleep(0.000001)

    def doBrightness(self):
        if self._waitingBrightness:
            self.do_set_brightness(self._waitingBrightnessValue)

    def push_to_driver(self):
        """Push the current pixel state to the driver"""
        self.waitForUpdate()
        self.doBrightness()

        if self._threadedUpdate:
            self._updateThread.update_colors()
        else:
            for d in self.drivers:
                d.update_colors()
            for d in self.drivers:
                d.sync()

    def lastThreadedUpdate(self):
        return max([d.lastUpdate for d in self.drivers])

    # use with caution!
    def set_colors(self, buf):
        """Use with extreme caution!
        Directly sets the internal buffer and bypasses all brightness and rotation control.
        buf must also be in the exact format required by the display type.
        """
        if len(self._colors) != len(buf):
            raise IOError("Data buffer size incorrect! "
                          "Expected: {} bytes / Received: {} bytes".format(
                              len(self._colors), len(buf)))
        self._colors[:] = buf

    def setBuffer(self, buf):
        """DEPRECATED!"""
        # https://stackoverflow.com/questions/1624883
        self.set_colors(buf=zip(*(iter(buf),) * 3))

    # Set the master brightness for the LEDs 0 - 255
    def _do_set_brightness(self, bright):
        self.waitForUpdate()
        for d in self.drivers:
            d.set_brightness(bright)

        self._waitingBrightnessValue = None
        self._waitingBrightness = False

    def set_brightness(self, bright):
        """Sets the master brightness scaling, 0 - 255

        If the driver supports it the brightness will be sent to the receiver directly.
        """
        if bright > 255 or bright < 0:
            raise ValueError('Brightness must be between 0 and 255')

        if self._threadedAnim:
            self._waitingBrightnessValue = bright
            self._waitingBrightness = True
        else:
            self._do_set_brightness(bright)

    # Set single pixel to RGB value
    def setRGB(self, pixel, r, g, b):
        """Set single pixel using individual RGB values instead of tuple"""
        self._set_base(pixel, (r, g, b))

    def setHSV(self, pixel, hsv):
        """Set single pixel to HSV tuple"""
        color = colors.hsv2rgb(hsv)
        self._set_base(pixel, color)

    # turns off the desired pixel
    def setOff(self, pixel):
        """Set single pixel off"""
        self._set_base(pixel, (0, 0, 0))

    def all_off(self):
        """Set all pixels off"""
        self._colors[:] = [(0, 0, 0)] * self.numLEDs

    # Fill the strand (or a subset) with a single color using a Color object
    def fill(self, color, start=0, end=-1):
        """Fill the entire strip with RGB color tuple"""
        start = max(start, 0)
        if end < 0 or end >= self.numLEDs:
            end = self.numLEDs - 1
        for led in range(start, end + 1):  # since 0-index include end in range
            self._set_base(led, color)

    # Fill the strand (or a subset) with a single color using RGB values
    def fillRGB(self, r, g, b, start=0, end=-1):
        """Fill entire strip by giving individual RGB values instead of tuple"""
        self.fill((r, g, b), start, end)

    # Fill the strand (or a subset) with a single color using HSV values
    def fillHSV(self, hsv, start=0, end=-1):
        """Fill the entire strip with HSV color tuple"""
        self.fill(colors.hsv2rgb(hsv), start, end)


class LEDStrip(LEDBase):

    def __init__(self, drivers, threadedUpdate=False, masterBrightness=255, pixelWidth=1):
        super().__init__(drivers, threadedUpdate, masterBrightness)

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
            self.numLEDs = self.numLEDs / self.pixelWidth

    # Set single pixel to Color value
    def _set(self, pixel, color):
        """Set pixel to RGB color tuple"""
        self._set_base(pixel, color)

    def _setScaled(self, pixel, color):
        start = pixel * self.pixelWidth
        for p in range(start, start + self.pixelWidth):
            self._set_base(p, color)

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
        result = zip(*result[::-1])

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
            self.matrix_map = zip(*self.matrix_map[::-1])

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

    def drawChar(self, x, y, c, color, bg, size, aa=False):
        matrix.draw_char(self.set, x, y, c, color, bg, size, aa)

    def drawText(self, text, x=0, y=0, color=None, bg=colors.Off, size=1, aa=False):
        matrix.draw_text(self.set, text, self.width,
                         self.height, x, y, color, bg, size, aa)


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
            buf = [color(i) for i in range(self.height)]
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

MANIFEST = [
    {
        "id": "strip",
        "class": LEDStrip,
        "type": "controller",
        "control_type": "strip",
        "display": "LEDStrip",
        "params": [{
                "id": "threadedUpdate",
                "label": "Threaded Update",
                "type": "bool",
                "default": False,
                "help": "Enable to run display updates on a separate thread, which can improve speed."
        }, {
            "id": "masterBrightness",
            "label": "Master Brightness",
            "type": "int",
            "min": 1,
            "max": 255,
            "default": 255,
            "help": "Master brightness for display, 0-255"
        }, {
            "id": "pixelWidth",
            "label": "Pixel Width",
            "group": "Advanced",
            "type": "int",
            "min": 1,
            "default": 1,
            "help": "Pixel scaling amount. Setting to >1 will make each logical pixel N LEDs in width."
        }, ]
    },
    {
        "id": "matrix",
        "class": LEDMatrix,
        "type": "controller",
        "control_type": "matrix",
        "display": "LEDMatrix",
        "params": [{
                "id": "width",
                "label": "Width",
                "type": "int",
                "default": 0,
                "min": 0,
                "help": "Width of display. Leave this and Height as 0 to get from driver."
        }, {
            "id": "height",
            "label": "Height",
            "type": "int",
            "default": 0,
            "min": 0,
            "help": "Height of display. Leave this and Width as 0 to get from driver."
        }, {
            "id": "rotation",
            "label": "Rotation",
            "type": "combo",
            "options": {
                    0: "0&deg;",
                    3: "90&deg;",
                    2: "180&deg;",
                    1: "270&deg;",
            },
            "default": 0,
            "help": "Amount to rotate matrix by."
        }, {
            "id": "vert_flip",
            "label": "Vertical Flip",
            "type": "bool",
            "default": False,
            "help": "Flip the display over the x-axis.",
        }, {
            "id": "serpentine",
            "label": "Serpentine",
            "type": "bool",
            "default": True,
            "help": "Use a serpentine layout for the pixel map when auto-generated.",
        }, {
            "id": "threadedUpdate",
            "label": "Threaded Update",
            "type": "bool",
            "default": False,
            "help": "Enable to run display updates on a separate thread, which can improve speed."
        }, {
            "id": "masterBrightness",
            "label": "Master Brightness",
            "type": "int",
            "min": 1,
            "max": 255,
            "default": 255,
            "help": "Master brightness for display, 0-255"
        }, {
            "id": "pixelSize",
            "label": "Pixel Size",
            "group": "Advanced",
            "type": "multi",
            "controls": [
                    {
                        "label": "Width",
                        "type": "int",
                        "min": 1,
                        "default": 1,
                        "help": "Logical Pixel Width"
                    }, {
                        "label": "Height",
                        "type": "int",
                        "min": 1,
                        "default": 1,
                        "help": "Logical Pixel Height"
                    },
            ],
            "default": [1, 1],
            "help":"Pixel scaling amount. Each logical pixel will be Width*Height LEDs in size."
        }, ]
    }
]
