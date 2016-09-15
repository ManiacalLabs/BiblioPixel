#!/usr/bin/env python
from __future__ import division
import colors
import time
import math
import font
import threading
import and_event


class updateDriverThread(threading.Thread):

    def __init__(self, driver):
        super(updateDriverThread, self).__init__()
        self.setDaemon(True)
        self._stop = threading.Event()
        self._wait = threading.Event()
        self._updating = threading.Event()
        self._reading = threading.Event()
        self._reading.set()
        self._data = []
        self._driver = driver

    def setData(self, data):
        self._reading.wait()
        self._data = data
        self._reading.clear()
        self._wait.set()

    def sync(self):
        self._updating.wait()
        self._driver.sync()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def sending(self):
        return self._wait.isSet()

    def run(self):
        while not self.stopped():
            self._wait.wait()
            self._updating.clear()
            self._driver._update(self._data)
            self._data = []
            self._wait.clear()
            self._reading.set()
            self._updating.set()


class updateThread(threading.Thread):

    def __init__(self, drivers):
        super(updateThread, self).__init__()
        self.setDaemon(True)
        self._stop = threading.Event()
        self._wait = threading.Event()
        self._reading = threading.Event()
        self._reading.set()
        self._data = []
        self._drivers = drivers
        for d in self._drivers:
            t = updateDriverThread(d)
            t.start()
            d._thread = t

        self._updated = and_event.AndEvent([d._thread._updating for d in self._drivers])

    def setData(self, data):
        assert len(data) == len(self._drivers), "Must have as many data blocks as drivers"
        self._reading.wait()
        self._data = data
        for i in range(len(data)):
            self._drivers[i]._thread.setData(data[i])
        self._reading.clear()
        self._wait.set()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        while not self.stopped():
            self._wait.wait()

            # while all([d._thread.sending() for d in self._drivers]):
            #     time.sleep(0.00000000001)

            self._updated.wait()
            # for d in self._drivers:
            #     d._thread._updating.wait()

            for d in self._drivers:
                d._thread.sync()

            self._updated.clear()

            self._data = []
            self._wait.clear()
            self._reading.set()


class LEDBase(object):

    def __init__(self, driver, threadedUpdate, masterBrightness):
        """Base LED class. Use LEDStrip or LEDMatrix instead!"""
        if not isinstance(driver, list):
            driver = [driver]

        self.driver = driver
        if not hasattr(self, 'numLEDs'):
            self.numLEDs = sum(d.numLEDs for d in self.driver)

        self.bufByteCount = int(3 * self.numLEDs)
        self._last_i = self.lastIndex = self.numLEDs - 1

        # This buffer will always be the same list - i.e. is guaranteed to only
        # be changed by list surgery, never assignment.
        self.buffer = [0] * self.bufByteCount

        self.masterBrightness = 255

        self._frameGenTime = 0
        self._frameTotalTime = None

        self._threadedUpdate = threadedUpdate

        if self._threadedUpdate:
            self._updateThread = updateThread(self.driver)
            self._updateThread.start()

        self._waitingBrightness = False
        self._waitingBrightnessValue = None
        self._threadedAnim = False

        self.setMasterBrightness(masterBrightness)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def cleanup(self):
        return self.__exit__(None, None, None)

    def _get_base(self, pixel):
        if pixel < 0 or pixel > self.lastIndex:
            return 0, 0, 0  # don't go out of bounds

        return (self.buffer[pixel * 3 + 0], self.buffer[pixel * 3 + 1], self.buffer[pixel * 3 + 2])

    def _set_base(self, pixel, color):
        try:
            if pixel < 0 or pixel > self._last_i:
                raise IndexError()

            if self.masterBrightness < 255:
                self.buffer[pixel * 3 +
                            0] = (color[0] * self.masterBrightness) >> 8
                self.buffer[pixel * 3 +
                            1] = (color[1] * self.masterBrightness) >> 8
                self.buffer[pixel * 3 +
                            2] = (color[2] * self.masterBrightness) >> 8
            else:
                self.buffer[pixel * 3:(pixel * 3) + 3] = color
        except IndexError:
            pass

    def waitForUpdate(self):
        if self._threadedUpdate:
            while all([d._thread.sending() for d in self.driver]):
                time.sleep(0.000001)

    def doBrightness(self):
        if self._waitingBrightness:
            self._doMasterBrigtness(self._waitingBrightnessValue)

    def update(self):
        """Push the current pixel state to the driver"""
        pos = 0
        self.waitForUpdate()
        self.doBrightness()
        if len(self.buffer) != self.bufByteCount:
            raise IOError("Data buffer size incorrect! Expected: {} bytes / Received: {} bytes".format(
                self.bufByteCount, len(self.buffer)))

        data = []
        for d in self.driver:
            data.append(self.buffer[pos:d.bufByteCount + pos])
            pos += d.bufByteCount
        if self._threadedUpdate:
            self._updateThread.setData(data)
        else:
            for i in range(len(self.driver)):
                self.driver[i]._update(data[i])
            for d in self.driver:
                d.sync()

    def lastThreadedUpdate(self):
        return max([d.lastUpdate for d in self.driver])

    # use with caution!
    def setBuffer(self, buf):
        """Use with extreme caution!
        Directly sets the internal buffer and bypasses all brightness and rotation control.
        buf must also be in the exact format required by the display type.
        """
        if len(buf) != self.bufByteCount:
            raise ValueError("For this display type and {0} LEDs, buffer must have {1} bytes but has {2}".format(
                self.bufByteCount / 3, self.bufByteCount, len(buf)))
        self.buffer[:] = buf

    # Set the master brightness for the LEDs 0 - 255
    def _doMasterBrigtness(self, bright):
        self.waitForUpdate()
        result = True
        for d in self.driver:
            if not d.setMasterBrightness(bright):
                result = False
                break

        # all or nothing, set them all back if False
        if not result:
            for d in self.driver:
                d.setMasterBrightness(255)
            self.masterBrightness = bright
        else:
            self.masterBrightness = 255

        self._waitingBrightnessValue = None
        self._waitingBrightness = False

    def setMasterBrightness(self, bright):
        """Sets the master brightness scaling, 0 - 255

        If the driver supports it the brightness will be sent to the receiver directly.
        """
        if bright > 255 or bright < 0:
            raise ValueError('Brightness must be between 0 and 255')

        if self._threadedAnim:
            self._waitingBrightnessValue = bright
            self._waitingBrightness = True
        else:
            self._doMasterBrigtness(bright)

    # Set single pixel to RGB value
    def setRGB(self, pixel, r, g, b):
        """Set single pixel using individual RGB values instead of tuple"""
        color = (r, g, b)
        self._set_base(pixel, color)

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
        self._resetBuffer()

    def _resetBuffer(self):
        self.buffer[:] = [0] * self.bufByteCount

    # Fill the strand (or a subset) with a single color using a Color object
    def fill(self, color, start=0, end=-1):
        """Fill the entire strip with RGB color tuple"""
        start = max(start, 0)
        if end < 0 or end > self.lastIndex:
            end = self.lastIndex
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

    def __init__(self, driver, threadedUpdate=False, masterBrightness=255, pixelWidth=1):
        super(LEDStrip, self).__init__(
            driver, threadedUpdate, masterBrightness)

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
            self.lastIndex = self.numLEDs - 1

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
        color = (r, g, b)
        self.set(pixel, color)

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

    def __init__(self, driver, width=0, height=0, coordMap=None, rotation=MatrixRotation.ROTATE_0, vert_flip=False, serpentine=True, threadedUpdate=False, masterBrightness=255, pixelSize=(1, 1)):
        """Main class for matricies.
        driver - instance that inherits from DriverBase
        width - X axis size of matrix
        height - Y axis size of matrix
        coordMap - a 2D matrix defining the X,Y to strip index mapping. Not needed in most cases
        rotation - how to rotate when generating the map. Not used if coordMap specified
        vert_flip - flips the generated map along the Y axis. This along with rotation can achieve any orientation
        """
        super(LEDMatrix, self).__init__(
            driver, threadedUpdate, masterBrightness)

        if width == 0 and height == 0:
            if len(self.driver) == 1:
                width = self.driver[0].width
                height = self.driver[0].height
            else:
                raise TypeError(
                    "Must provide width and height if using multiple drivers!")

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
            if len(self.driver) == 1:
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
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                raise IndexError()
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
        f = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x = 0
        y = r

        self.set(x0, y0 + r, color)
        self.set(x0, y0 - r, color)
        self.set(x0 + r, y0, color)
        self.set(x0 - r, y0, color)

        while x < y:
            if f >= 0:
                y -= 1
                ddF_y += 2
                f += ddF_y
            x += 1
            ddF_x += 2
            f += ddF_x

            self.set(x0 + x, y0 + y, color)
            self.set(x0 - x, y0 + y, color)
            self.set(x0 + x, y0 - y, color)
            self.set(x0 - x, y0 - y, color)
            self.set(x0 + y, y0 + x, color)
            self.set(x0 - y, y0 + x, color)
            self.set(x0 + y, y0 - x, color)
            self.set(x0 - y, y0 - x, color)

    def _drawCircleHelper(self, x0, y0, r, cornername, color=None):
        f = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x = 0
        y = r

        while x < y:
            if (f >= 0):
                y -= 1
                ddF_y += 2
                f += ddF_y
            x += 1
            ddF_x += 2
            f += ddF_x
            if (cornername & 0x4):
                self.set(x0 + x, y0 + y, color)
                self.set(x0 + y, y0 + x, color)

            if (cornername & 0x2):
                self.set(x0 + x, y0 - y, color)
                self.set(x0 + y, y0 - x, color)

            if (cornername & 0x8):
                self.set(x0 - y, y0 + x, color)
                self.set(x0 - x, y0 + y, color)

            if (cornername & 0x1):
                self.set(x0 - y, y0 - x, color)
                self.set(x0 - x, y0 - y, color)

    def _fillCircleHelper(self, x0, y0, r, cornername, delta, color=None):
        f = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x = 0
        y = r

        while (x < y):
            if (f >= 0):
                y -= 1
                ddF_y += 2
                f += ddF_y
            x += 1
            ddF_x += 2
            f += ddF_x

            if (cornername & 0x1):
                self._drawFastVLine(x0 + x, y0 - y, 2 * y + 1 + delta, color)
                self._drawFastVLine(x0 + y, y0 - x, 2 * x + 1 + delta, color)

            if (cornername & 0x2):
                self._drawFastVLine(x0 - x, y0 - y, 2 * y + 1 + delta, color)
                self._drawFastVLine(x0 - y, y0 - x, 2 * x + 1 + delta, color)

    def fillCircle(self, x0, y0, r, color=None):
        """Draws a filled circle at point x0,y0 with radius r and specified color"""
        self._drawFastVLine(x0, y0 - r, 2 * r + 1, color)
        self._fillCircleHelper(x0, y0, r, 3, 0, color)

    def drawLine(self, x0, y0, x1, y1, color=None, colorFunc=None, aa=False):
        if aa:
            self.wu_line(x0, y0, x1, y1, color, colorFunc)
        else:
            self.bresenham_line(x0, y0, x1, y1, color, colorFunc)

    # Bresenham's algorithm
    def bresenham_line(self, x0, y0, x1, y1, color=None, colorFunc=None):
        """Draw line from point x0,y0 to x,1,y1. Will draw beyond matrix bounds."""
        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = x1 - x0
        dy = abs(y1 - y0)

        err = dx / 2

        if y0 < y1:
            ystep = 1
        else:
            ystep = -1

        count = 0
        for x in range(x0, x1 + 1):
            if colorFunc:
                color = colorFunc(count)
                count += 1

            if steep:
                self.set(y0, x, color)
            else:
                self.set(x, y0, color)

            err -= dy
            if err < 0:
                y0 += ystep
                err += dx
    # END Bresenham's algorithm

    # Xiaolin Wu's Line Algorithm
    def wu_line(self, x0, y0, x1, y1, color=None, colorFunc=None):
        funcCount = [0]  # python2 hack since nonlocal not available

        def plot(x, y, level):
            c = color
            if colorFunc:
                c = colorFunc(funcCount[0])
                funcCount[0] += 1

            c = colors.color_scale(color, int(255 * level))
            self.set(int(x), int(y), c)

        def ipart(x):
            return int(x)

        def fpart(x):
            return x - math.floor(x)

        def rfpart(x):
            return 1.0 - fpart(x)

        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = x1 - x0
        dy = y1 - y0
        gradient = dy / dx

        # handle first endpoint
        xend = round(x0)
        yend = y0 + gradient * (xend - x0)
        xgap = rfpart(x0 + 0.5)
        xpxl1 = xend  # this will be used in the main loop
        ypxl1 = ipart(yend)

        if steep:
            plot(ypxl1, xpxl1, rfpart(yend) * xgap)
            plot(ypxl1 + 1, xpxl1, fpart(yend) * xgap)
        else:
            plot(xpxl1, ypxl1, rfpart(yend) * xgap)
            plot(xpxl1, ypxl1 + 1, fpart(yend) * xgap)

        # first y-intersection for the main loop
        intery = yend + gradient

        # handle second endpoint
        xend = round(x1)
        yend = y1 + gradient * (xend - x1)
        xgap = fpart(x1 + 0.5)
        xpxl2 = xend  # this will be used in the main loop
        ypxl2 = ipart(yend)

        if steep:
            plot(ypxl2, xpxl2, rfpart(yend) * xgap)
            plot(ypxl2 + 1, xpxl2, fpart(yend) * xgap)
        else:
            plot(xpxl2, ypxl2, rfpart(yend) * xgap)
            plot(xpxl2, ypxl2 + 1, fpart(yend) * xgap)

        # main loop
        for x in range(int(xpxl1 + 1), int(xpxl2)):
            if steep:
                plot(ipart(intery), x, rfpart(intery))
                plot(ipart(intery) + 1, x, fpart(intery))
            else:
                plot(x, ipart(intery), rfpart(intery))
                plot(x, ipart(intery) + 1, fpart(intery))
            intery = intery + gradient

    # END Xiaolin Wu's Line Algorithm

    def _drawFastVLine(self, x, y, h, color=None, aa=False):
        self.drawLine(x, y, x, y + h - 1, color, aa)

    def _drawFastHLine(self, x, y, w, color=None, aa=False):
        self.drawLine(x, y, x + w - 1, y, color, aa)

    def drawRect(self, x, y, w, h, color=None, aa=False):
        """Draw rectangle with top-left corner at x,y, width w and height h"""
        self._drawFastHLine(x, y, w, color, aa)
        self._drawFastHLine(x, y + h - 1, w, color, aa)
        self._drawFastVLine(x, y, h, color, aa)
        self._drawFastVLine(x + w - 1, y, h, color, aa)

    def fillRect(self, x, y, w, h, color=None, aa=False):
        """Draw solid rectangle with top-left corner at x,y, width w and height h"""
        for i in range(x, x + w):
            self._drawFastVLine(i, y, h, color, aa)

    def fillScreen(self, color=None):
        """Fill the matrix with the given RGB color"""
        self.fillRect(0, 0, self.width, self.height, color)

    def drawRoundRect(self, x, y, w, h, r, color=None, aa=False):
        """Draw rectangle with top-left corner at x,y, width w, height h, and corner radius r"""
        self._drawFastHLine(x + r, y, w - 2 * r, color, aa)  # Top
        self._drawFastHLine(x + r, y + h - 1, w - 2 * r, color, aa)  # Bottom
        self._drawFastVLine(x, y + r, h - 2 * r, color, aa)  # Left
        self._drawFastVLine(x + w - 1, y + r, h - 2 * r, color, aa)  # Right
        # draw four corners
        self._drawCircleHelper(x + r, y + r, r, 1, color, aa)
        self._drawCircleHelper(x + w - r - 1, y + r, r, 2, color, aa)
        self._drawCircleHelper(x + w - r - 1, y + h - r - 1, r, 4, color, aa)
        self._drawCircleHelper(x + r, y + h - r - 1, r, 8, color, aa)

    def fillRoundRect(self, x, y, w, h, r, color=None, aa=False):
        """Draw solid rectangle with top-left corner at x,y, width w, height h, and corner radius r"""
        self.fillRect(x + r, y, w - 2 * r, h, color, aa)
        self._fillCircleHelper(x + w - r - 1, y + r, r,
                               1, h - 2 * r - 1, color, aa)
        self._fillCircleHelper(x + r, y + r, r, 2, h - 2 * r - 1, color, aa)

    def drawTriangle(self, x0, y0, x1, y1, x2, y2, color=None, aa=False):
        """Draw triangle with points x0,y0 - x1,y1 - x2,y2"""
        self.drawLine(x0, y0, x1, y1, color, aa)
        self.drawLine(x1, y1, x2, y2, color, aa)
        self.drawLine(x2, y2, x0, y0, color, aa)

    def fillTrangle(self, x0, y0, x1, y1, x2, y2, color=None, aa=False):
        """Draw solid triangle with points x0,y0 - x1,y1 - x2,y2"""
        a = b = y = last = 0

        if y0 > y1:
            y0, y1 = y1, y0
            x0, x1 = x1, x0
        if y1 > y2:
            y2, y1 = y1, y2
            x2, x1 = x1, x2
        if y0 > y1:
            y0, y1 = y1, y0
            x0, x1 = x1, x0

        if y0 == y2:  # Handle awkward all-on-same-line case as its own thing
            a = b = x0
            if x1 < a:
                a = x1
            elif x1 > b:
                b = x1
            if x2 < a:
                a = x2
            elif x2 > b:
                b = x2
            self._drawFastHLine(a, y0, b - a + 1, color, aa)

        dx01 = x1 - x0
        dy01 = y1 - y0
        dx02 = x2 - x0
        dy02 = y2 - y0
        dx12 = x2 - x1
        dy12 = y2 - y1
        sa = 0
        sb = 0

        # For upper part of triangle, find scanline crossings for segments
        # 0-1 and 0-2.  If y1=y2 (flat-bottomed triangle), the scanline y1
        # is included here (and second loop will be skipped, avoiding a /0
        # error there), otherwise scanline y1 is skipped here and handled
        # in the second loop...which also avoids a /0 error here if y0=y1
        # (flat-topped triangle).

        if y1 == y2:
            last = y1  # include y1 scanline
        else:
            last = y1 - 1  # skip it

        for y in range(y, last + 1):
            a = x0 + sa / dy01
            b = x0 + sb / dy02
            sa += dx01
            sb += dx02

            if a > b:
                a, b = b, a
            self._drawFastHLine(a, y, b - a + 1, color, aa)

        # For lower part of triangle, find scanline crossings for segments
        # 0-2 and 1-2.  This loop is skipped if y1=y2.
        sa = dx12 * (y - y1)
        sb = dx02 * (y - y0)

        for y in range(y, y2 + 1):
            a = x1 + sa / dy12
            b = x0 + sb / dy02
            sa += dx12
            sb += dx02

            if a > b:
                a, b = b, a
            self._drawFastHLine(a, y, b - a + 1, color, aa)

    def drawChar(self, x, y, c, color, bg, aa=False, font=font.default_font, font_scale=1):
        assert font_scale >= 1, "font_scale must be >= 1"
        f = self.fonts[font]
        fh = f['height']
        FONT = f['data']

        c = ord(c)  # make it the int value
        if c < f['bounds'][0] or c > f['bounds'][1]:
            c_data = f['undef']
        else:
            c_data = FONT[c - f['bounds'][0]]

        fw = len(c_data)
        for i in range(fw + f['sep']):
            xPos = x + (i * font_scale)
            if ((xPos < self.width) and (xPos + fw * font_scale - 1) >= 0):
                if i >= fw:
                    line = 0
                else:
                    line = FONT[c][i]
                for j in range(fh):
                    yPos = y + (j * font_scale)
                    if ((yPos < self.height) and
                            (yPos + fh * font_scale - 1) >= 0):
                        if line & 0x1:
                            if font_scale == 1:
                                self.set(xPos, yPos, color)
                            else:
                                self.fillRect(xPos, yPos, font_scale, font_scale, color, aa)
                        elif bg != color and bg is not None:
                            if font_scale == 1:
                                self.set(xPos, yPos, bg)
                            else:
                                self.fillRect(xPos, yPos, font_scale, font_scale, bg, aa)
                    line >>= 1
        return fw + f['sep']

    def drawText(self, text, x=0, y=0, color=None, bg=colors.Off, aa=False, font=font.default_font, font_scale=1):
        fh = self.fonts[font]['height']
        for c in text:
            if c == '\n':
                y += font_scale * fh
                x = 0
            elif c == '\r':
                pass  # skip it
            else:
                fw = self.drawChar(x, y, c, color, bg, aa, font, font_scale)
                x += font_scale * fw
                if x >= self.width:
                    break

# Takes a matrix and displays it as individual columns over time


class LEDPOV(LEDMatrix):

    def __init__(self, driver, povHeight, width, rotation=MatrixRotation.ROTATE_0, vert_flip=False, threadedUpdate=False, masterBrightness=255):
        self.numLEDs = povHeight * width

        super(LEDPOV, self).__init__(driver, width, povHeight, None,
                                     rotation, vert_flip, threadedUpdate, masterBrightness)

    # This is the magic. Overriding the normal update() method
    # It will automatically break up the frame into columns spread over
    # frameTime (ms)
    def update(self, frameTime=None):
        if frameTime:
            self._frameTotalTime = frameTime

        sleep = None
        if self._frameTotalTime:
            sleep = (self._frameTotalTime - self._frameGenTime) / self.width

        width = self.width
        for h in range(width):
            start = time.time() * 1000.0

            buf = [item for sublist in [self.buffer[(width * i * 3) + (h * 3):(
                width * i * 3) + (h * 3) + (3)] for i in range(self.height)] for item in sublist]
            self.driver[0].update(buf)
            sendTime = (time.time() * 1000.0) - start
            if sleep:
                time.sleep(max(0, (sleep - sendTime) / 1000.0))


class LEDCircle(LEDBase):

    def __init__(self, driver, rings, maxAngleDiff=0, rotation=0, threadedUpdate=False, masterBrightness=255):
        super(LEDCircle, self).__init__(
            driver, threadedUpdate, masterBrightness)
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
