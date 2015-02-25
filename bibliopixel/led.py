#!/usr/bin/env python
import colors
import time
import math
import font
import time
import threading

class updateThread(threading.Thread):

    def __init__(self, driver):
        super(updateThread, self).__init__()
        self.setDaemon(True)
        self._stop = threading.Event()
        self._wait = threading.Event()
        self._data = []
        self._driver = driver

    def setData(self, data):
        self._data = data
        self._wait.set()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def sending(self):
        return self._wait.isSet()

    def run(self):
        while not self.stopped():
            self._wait.wait()
            self._driver._update(self._data)
            self._data = []
            self._wait.clear()
            
class LEDBase(object):

    def __init__(self, driver, threadedUpdate):
        """Base LED class. Use LEDStrip or LEDMatrix instead!"""
        if not isinstance(driver, list):
            driver = [driver]

        self.driver = driver
        try:
            self.numLEDs
        except AttributeError as e:
            self.numLEDs = 0
            for d in self.driver:
                self.numLEDs += d.numLEDs

        self.bufByteCount = int(3 * self.numLEDs)
        self.lastIndex = self.numLEDs - 1
        
        self.buffer = [0 for x in range(self.bufByteCount)]
        
        self.masterBrightness = 255

        self._frameGenTime = 0
        self._frameTotalTime = None

        self._threadedUpdate = threadedUpdate

        if self._threadedUpdate:
            for d in self.driver:
                t = updateThread(d)
                t.start()
                d._thread = t

    def _get_base(self, pixel):
        if(pixel < 0 or pixel > self.lastIndex):
            return (0,0,0) #don't go out of bounds

        return (self.buffer[pixel*3 + 0], self.buffer[pixel*3 + 1], self.buffer[pixel*3 + 2])

    def _set_base(self, pixel, color):
        if(pixel < 0 or pixel > self.lastIndex):
            return; #don't go out of bounds

        if self.masterBrightness < 255:
            self.buffer[pixel*3 + 0] = (color[0] * self.masterBrightness) >> 8
            self.buffer[pixel*3 + 1] = (color[1] * self.masterBrightness) >> 8
            self.buffer[pixel*3 + 2] = (color[2] * self.masterBrightness) >> 8
        else:
            self.buffer[pixel*3:(pixel*3)+3] = list(color)

    def update(self):
        """Push the current pixel state to the driver"""
        pos = 0
        if self._threadedUpdate:
            while all([d._thread.sending() for d in self.driver]):
                time.sleep(0.000001)

        for d in self.driver:
            if self._threadedUpdate:
                d._thread.setData(self.buffer[pos:d.bufByteCount+pos])
            else:
                d._update(self.buffer[pos:d.bufByteCount+pos])
            pos += d.bufByteCount
    
    def lastThreadedUpdate(self):
        return max([d.lastUpdate for d in self.driver])

    #use with caution!
    def setBuffer(self, buf):
        """Use with extreme caution!
        Directly sets the internal buffer and bypasses all brightness and rotation control.
        buf must also be in the exact format required by the display type.
        """
        if len(buf) != self.bufByteCount:
            raise ValueError("For this display type and {0} LEDs, buffer must have {1} bytes but only has {2}".format(self.numLEDs, self.bufByteCount, len(buf)))
        self.buffer = buf

    #Set the master brightness for the LEDs 0 - 255
    def setMasterBrightness(self, bright):
        """Sets the master brightness scaling, 0 - 255

        If the driver supports it the brightness will be sent to the receiver directly.
        """
        if(bright > 255 or bright < 0):
            raise ValueError('Brightness must be between 0 and 255')
        result = True
        for d in self.driver:
            if(not d.setMasterBrightness(bright)):
                result = False
                break

        #all or nothing, set them all back if False
        if not result:
            for d in self.driver:
                d.setMasterBrightness(255)
            self.masterBrightness = bright
        else:
            self.masterBrightness = 255
    
    #Set single pixel to RGB value
    def setRGB(self, pixel, r, g, b):
        """Set single pixel using individual RGB values instead of tuple"""
        color = (r, g, b)
        self._set_base(pixel, color)

    def setHSV(self, pixel, hsv):
        """Set single pixel to HSV tuple"""
        color = colors.hsv2rgb(hsv)
        self._set_base(pixel, color)
        
    #turns off the desired pixel
    def setOff(self, pixel):
        """Set single pixel off"""
        self._set_base(pixel, (0, 0, 0))

    def all_off(self):
       """Set all pixels off"""
       self._resetBuffer()

    def _resetBuffer(self):
        self.buffer = [0 for x in range(self.bufByteCount)]

class LEDStrip(LEDBase):

    def __init__(self, driver, threadedUpdate = False):
        super(LEDStrip, self).__init__(driver, threadedUpdate)

    #Fill the strand (or a subset) with a single color using a Color object
    def fill(self, color, start=0, end=-1):
        """Fill the entire strip with RGB color tuple"""
        if start < 0:
            start = 0
        if end < 0 or end > self.lastIndex:
            end = self.lastIndex
        for led in range(start, end + 1): #since 0-index include end in range
            self.set(led, color)

    #Fill the strand (or a subset) with a single color using RGB values
    def fillRGB(self, r, g, b, start=0, end=-1):
        """Fill entire strip by giving individual RGB values instead of tuple"""
        self.fill((r, g, b), start, end)
        
    #Fill the strand (or a subset) with a single color using HSV values
    def fillHSV(self, hsv, start=0, end=-1):
        """Fill the entire strip with HSV color tuple"""
        self.fill(colors.hsv2rgb(hsv), start, end)

    #Set single pixel to Color value
    def set(self, pixel, color):
        """Set pixel to RGB color tuple"""
        self._set_base(pixel, color)

    def get(self, pixel):
        """Get RGB color tuple of color at index pixel"""
        return self._get_base(pixel)

class MatrixRotation:
    ROTATE_0 = 0   #no rotation
    ROTATE_90 = 3  #rotate 90 degrees
    ROTATE_180 = 2 #rotate 180 degrees
    ROTATE_270 = 1 #rotate 270 degrees

def mapGen(width, height, serpentine = True, offset = 0, rotation = MatrixRotation.ROTATE_0, vert_flip=False):
    """Helper method to generate X,Y coordinate maps for strips"""

    result = []
    for y in range(height):
        if not serpentine or y % 2 == 0:
            result.append([(width * y) + x + offset for x in range(width)])
        else:
            result.append([((width * (y+1)) - 1) - x + offset for x in range(width)])

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
            offsets.append(h*len(m[0]) + offsets[count])
            count += 1

        for y in range(h):
            self.map.append([])
            for x in range(len(maps)):
                self.map[y + yOff] += [i + offsets[x] for i in maps[x][y]]

        self.offset = offsets[len(offsets)-1]
        
class LEDMatrix(LEDBase):

    def __init__(self, driver, width = 0, height = 0, coordMap = None, rotation = MatrixRotation.ROTATE_0, vert_flip = False, serpentine = True, threadedUpdate = False):
        """Main class for matricies.
        driver - instance that inherits from DriverBase
        width - X axis size of matrix
        height - Y axis size of matrix
        coordMap - a 2D matrix defining the X,Y to strip index mapping. Not needed in most cases
        rotation - how to rotate when generating the map. Not used if coordMap specified
        vert_flip - flips the generated map along the Y axis. This along with rotation can achieve any orientation
        """
        super(LEDMatrix, self).__init__(driver, threadedUpdate)

        if width == 0 and height == 0:
            if len(self.driver) == 1:
                width = self.driver[0].width
                height = self.driver[0].height
            else:
                raise TypeError("Must provide width and height if using multiple drivers!")

        self.width = width
        self.height = height

        #if both are 0 try to assume it's a square display
        if self.width == 0 and self.height == 0:
            square = int(math.sqrt(self.numLEDs))
            if (square * square) == self.numLEDs:
                self.width = self.height = square
            else:
                raise TypeError("No width or height passed but the number of LEDs is not a perfect square")

        if self.width * self.height != self.numLEDs:
            raise TypeError("width * height MUST equal the total pixel count!")

        if coordMap:
            self.matrix_map = coordMap
        else:
            if len(self.driver) == 1:
                self.matrix_map = mapGen(self.width, self.height, serpentine)
            else:
                raise TypeError("Must provide coordMap if using multiple drivers!")

        #apply rotation
        for i in range(rotation):
            self.matrix_map = zip(*self.matrix_map[::-1])

        #apply flip
        if vert_flip:
            self.matrix_map = self.matrix_map[::-1]

        #if 90 or 270 rotation dimensions need to be swapped so they match the matrix rotation
        if rotation % 2 != 0:
            w = self.width
            h = self.height
            self.width = h
            self.height = w

    #Set single pixel to Color value
    def set(self, x, y, color):
        """Sets the pixel at x,y with an RGB tuple: (r, g, b)"""
        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return #just throw out anything out of bounds

        pixel = self.matrix_map[y][x]
        self._set_base(pixel, color)

    def get(self, x, y):
        """Gets the color of the pixel at x,y"""
        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return (0,0,0)#just throw out anything out of bounds

        pixel = self.matrix_map[y][x]
        return self._get_base(pixel)

    def setHSV(self, x, y, hsv):
        """Set the pixel at x,y with an HSV tuple: (h, s, v)"""
        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return #just throw out anything out of bounds

        pixel = self.matrix_map[y][x]
        super(LEDMatrix, self).setHSV(pixel, hsv)

    def setRGB(self, x, y, r, g, b):
        """Set the pixel at x,y with individual RGB values"""
        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return #just throw out anything out of bounds

        pixel = self.matrix_map[y][x]
        super(LEDMatrix, self).setRGB(pixel, r, g, b)


    ###############################################################################
    # Drawing Functions
    # Lovingly borrowed from Adafruit
    # https://github.com/adafruit/Adafruit-GFX-Library/blob/master/Adafruit_GFX.cpp
    ###############################################################################

    def drawCircle(self, x0, y0, r, color):
        """Draws a circle at point x0, y0 with radius r of the specified RGB color"""
        f = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x = 0
        y = r

        self.set(x0, y0+r, color)
        self.set(x0, y0-r, color)
        self.set(x0+r, y0, color)
        self.set(x0-r, y0, color)

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

    def _drawCircleHelper(self, x0, y0, r, cornername, color):
        f     = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x     = 0
        y     = r

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
    
    def _fillCircleHelper(self, x0, y0, r, cornername, delta, color):
        f     = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x     = 0
        y     = r

        while (x<y):
            if (f >= 0):
              y -= 1
              ddF_y += 2
              f += ddF_y
            x += 1
            ddF_x += 2
            f += ddF_x

            if (cornername & 0x1):
              self._drawFastVLine(x0+x, y0-y, 2*y+1+delta, color)
              self._drawFastVLine(x0+y, y0-x, 2*x+1+delta, color)
            
            if (cornername & 0x2):
              self._drawFastVLine(x0-x, y0-y, 2*y+1+delta, color)
              self._drawFastVLine(x0-y, y0-x, 2*x+1+delta, color)

    def fillCircle(self, x0, y0, r, color):
        """Draws a filled circle at point x0,y0 with radius r and specified color"""
        self._drawFastVLine(x0, y0-r, 2*r+1, color)
        self._fillCircleHelper(x0, y0, r, 3, 0, color)

    #Bresenham's algorithm - thx wikpedia
    def drawLine(self, x0, y0, x1, y1, color):
        """Draw line from point x0,y0 to x,1,y1. Will draw beyond matrix bounds."""
        steep = abs(y1-y0) > abs(x1-x0)
        if steep:
            x0,y0 = y0,x0
            x1,y1 = y1,x1

        if x0 > x1:
            x0,x1 = x1,x0
            y0,y1 = y1,y0

        dx = x1 - x0
        dy = abs(y1 - y0)

        err = dx / 2

        if y0 < y1:
            ystep = 1
        else:
            ystep = -1

        for x in range(x0, x1+1):
            if steep:
                self.set(y0, x, color)
            else:
                self.set(x, y0, color)

            err -= dy
            if err < 0:
                y0 += ystep
                err += dx

    def _drawFastVLine(self, x, y, h, color):
        self.drawLine(x, y, x, y+h-1, color)

    def _drawFastHLine(self, x, y, w, color):
        self.drawLine(x, y, x+w-1, y, color)

    def drawRect(self, x, y, w, h, color):
        """Draw rectangle with top-left corner at x,y, width w and height h"""
        self._drawFastHLine(x, y, w, color)
        self._drawFastHLine(x, y+h-1, w, color)
        self._drawFastVLine(x, y, h, color)
        self._drawFastVLine(x+w-1, y, h, color)

    def fillRect(self, x, y, w, h, color):
        """Draw solid rectangle with top-left corner at x,y, width w and height h"""
        for i in range(x, x+w):
            self._drawFastVLine(i, y, h, color)

    def fillScreen(self, color):
        """Fill the matrix with the given RGB color"""
        self.fillRect(0, 0, self.width, self.height, color)

    def drawRoundRect(self, x, y, w, h, r, color):
        """Draw rectangle with top-left corner at x,y, width w, height h, and corner radius r"""
        self._drawFastHLine(x+r  , y    , w-2*r, color) #Top
        self._drawFastHLine(x+r  , y+h-1, w-2*r, color) #Bottom
        self._drawFastVLine(x    , y+r  , h-2*r, color) #Left
        self._drawFastVLine(x+w-1, y+r  , h-2*r, color) #Right
        #draw four corners
        self._drawCircleHelper(x+r    , y+r    , r, 1, color)
        self._drawCircleHelper(x+w-r-1, y+r    , r, 2, color)
        self._drawCircleHelper(x+w-r-1, y+h-r-1, r, 4, color)
        self._drawCircleHelper(x+r    , y+h-r-1, r, 8, color)

    def fillRoundRect(self, x, y, w, h, r, color):
        """Draw solid rectangle with top-left corner at x,y, width w, height h, and corner radius r"""
        self.fillRect(x+r, y, w-2*r, h, color)
        self._fillCircleHelper(x+w-r-1, y+r, r, 1, h-2*r-1, color)
        self._fillCircleHelper(x+r    , y+r, r, 2, h-2*r-1, color)

    def drawTriangle(self, x0, y0, x1, y1, x2, y2, color):
        """Draw triangle with points x0,y0 - x1,y1 - x2,y2"""
        self.drawLine(x0, y0, x1, y1, color)
        self.drawLine(x1, y1, x2, y2, color)
        self.drawLine(x2, y2, x0, y0, color)  

    def fillTrangle(self, x0, y0, x1, y1, x2, y2, color):
        """Draw solid triangle with points x0,y0 - x1,y1 - x2,y2"""
        a = b = y = last = 0

        if y0 > y1:
            y0,y1 = y1,y0
            x0,x1 = x1,x0
        if y1 > y2:
            y2,y1 = y1,y2
            x2,x1 = x1,x2
        if y0 > y1:
            y0,y1 = y1,y0
            x0,x1 = x1,x0

        if y0 == y2: #Handle awkward all-on-same-line case as its own thing
            a = b = x0
            if x1 < a: a = x1
            elif x1 > b: b = x1
            if x2 < a: a = x2
            elif x2 > b: b = x2
            self._drawFastHLine(a, y0, b-a+1, color)

        dx01 = x1 - x0
        dy01 = y1 - y0
        dx02 = x2 - x0
        dy02 = y2 - y0
        dx12 = x2 - x1
        dy12 = y2 - y1
        sa = 0
        sb = 0

        #For upper part of triangle, find scanline crossings for segments
        #0-1 and 0-2.  If y1=y2 (flat-bottomed triangle), the scanline y1
        #is included here (and second loop will be skipped, avoiding a /0
        #error there), otherwise scanline y1 is skipped here and handled
        #in the second loop...which also avoids a /0 error here if y0=y1
        #(flat-topped triangle).

        if y1 == y2: last = y1 #include y1 scanline
        else:        last = y1-1 #skip it

        for y in range(y, last+1):
            a = x0 + sa / dy01
            b = x0 + sb / dy02
            sa += dx01
            sb += dx02

            if a > b: a,b = b,a
            self._drawFastHLine(a, y, b-a+1, color)

        #For lower part of triangle, find scanline crossings for segments
        #0-2 and 1-2.  This loop is skipped if y1=y2.
        sa = dx12 * (y - y1)
        sb = dx02 * (y - y0)

        for y in range(y, y2+1):
            a   = x1 + sa / dy12
            b   = x0 + sb / dy02
            sa += dx12
            sb += dx02

            if a > b: a,b = b,a
            self._drawFastHLine(a, y, b-a+1, color)

    def drawChar(self, x, y, c, color, bg, size):
        c = ord(c) #make it the int value
        for i in range(6):
            xPos = x+(i*size)
            if ((xPos < self.width) and
                (xPos + 6 * size -1) >= 0):
                
                if i == 5:
                    line = 0
                else:
                    line = font.GLCDFONT[c][i]
                for j in range(8):
                    yPos = y+(j*size)
                    if ((yPos < self.height) and
                        (yPos + 8 * size -1) >= 0):
                        if line & 0x1:
                            if size == 1:
                                self.set(xPos, yPos, color)
                            else:
                                self.fillRect(xPos, yPos, size, size, color)
                        elif bg != color:
                            if size == 1:
                                self.set(xPos, yPos, bg)
                            else:
                                self.fillRect(xPos, yPos, size, size, bg)
                    line >>= 1
        
    def drawText(self, text, x = 0, y = 0, color = colors.White, bg = colors.Off, size = 1):
        for c in text:
            if c == '\n':
                pass
                y += size*8
                x = 0
            elif c == '\r':
                pass #skip it
            else:
                self.drawChar(x, y, c, color, bg, size)
                x += size*6
                if x >= self.width:
                    break

