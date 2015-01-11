from bibliopixel import LEDMatrix
from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors

import math
import time
import random

def genVector(width, height, x_mult = 1, y_mult = 1):
    """Generates a map of vector lengths from the center point to each coordinate
    
    widht - width of matrix to generate
    height - height of matrix to generate
    x_mult - value to scale x-axis by 
    y_mult - value to scale y-axis by 
    """
    centerX = (width - 1) / 2.0
    centerY = (height - 1) / 2.0

    return [[int(math.sqrt(math.pow(x - centerX, 2*x_mult) + math.pow(y - centerY, 2*y_mult))) for x in range(width)] for y in range(height)]

def pointOnCircle(cx, cy, radius, angle):
    """Calculates the coordinates of a point on a circle given the center point, radius, and angle"""
    angle = math.radians(angle) - (math.pi / 2)
    x = cx + radius * math.cos(angle)
    if x < cx:
        x = math.ceil(x)
    else:
        x = math.floor(x)

    y = cy + radius * math.sin(angle)

    if y < cy:
        y = math.ceil(y)
    else:
        y = math.floor(y)

    return (int(x), int(y))

class Bloom(BaseMatrixAnim):

    def __init__(self, led, dir = True):
        super(Bloom, self).__init__(led)
        self._vector = genVector(self._led.width, self._led.height)
        self._dir = dir

    def step(self, amt = 8):
        if self._dir:
            s = 255 - self._step
        else:
            s = self._step

        h = self._led.height
        w = self._led.width

        #this ignores master brightness in the interest of speed
        # buf = [colors.hue_helper(self._vector[y][x], h, s) for y in range(h) for x in range(w)]
        # buf = [i for sub in buf for i in sub]
        # self._led.setBuffer(buf)

        #this respects master brightness but is slower
        for y in range(self._led.height):
           for x in range(self._led.width):
               c = colors.hue_helper(self._vector[y][x], self._led.height, s)
               self._led.set(x, y, c)

        self._step += amt
        if(self._step >= 255):
            self._step = 0

class AnalogClock(BaseMatrixAnim):
    def __init__(self, led):
        super(AnalogClock, self).__init__(led)
        self._centerX = (self._led.width - 1) / 2
        self._centerY = (self._led.height - 1) / 2

    def step(self, amt = 1):
        self._led.all_off()
        t = time.localtime()
        hrs = t.tm_hour % 12
        min = t.tm_min
        sec = t.tm_sec

        p_hrs = pointOnCircle(self._centerX, self._centerY, int(self._centerX *0.7), hrs * 30)
        p_min = pointOnCircle(self._centerX, self._centerY, self._centerX, min * 6)
        p_sec = pointOnCircle(self._centerX, self._centerY, self._centerX, sec * 6)

        self._led.drawLine(self._centerX, self._centerY, p_hrs[0], p_hrs[1], (255, 0, 0))
        self._led.drawLine(self._centerX, self._centerY, p_min[0], p_min[1], (0, 255, 0))
        self._led.drawLine(self._centerX, self._centerY, p_sec[0], p_sec[1], (0, 0, 255))
        
        self._step = 0

class RGBAnalogClock(BaseMatrixAnim):

    def __init__(self, led):
        super(RGBAnalogClock, self).__init__(led)
        self._centerX = (self._led.width - 1) / 2
        self._centerY = (self._led.height - 1) / 2

    def step(self, amt = 1):
        self._led.all_off()
        t = time.localtime()
        hrs = t.tm_hour % 12
        min = t.tm_min
        sec = t.tm_sec

        p_hrs = pointOnCircle(self._centerX, self._centerY, int(self._centerX * 0.7), hrs * 30)
        p_min = pointOnCircle(self._centerX, self._centerY, self._centerX, min * 6)
        p_sec = pointOnCircle(self._centerX, self._centerY, self._centerX, sec * 6)

        c_hrs = colors.hue2rgb_rainbow(t.tm_hour * (256/24))

        c_min = colors.hue2rgb_rainbow(min * (256/60))

        c_sec = colors.hue2rgb_rainbow(sec * (256/60))

        self._led.drawLine(self._centerX, self._centerY, p_hrs[0], p_hrs[1], c_hrs)
        self._led.drawLine(self._centerX, self._centerY, p_min[0], p_min[1], c_min)
        self._led.drawLine(self._centerX, self._centerY, p_sec[0], p_sec[1], c_sec)
        
        self._step = 0

class MatrixRain(BaseMatrixAnim):

    def __init__(self, led, colors=[colors.Green], tail=4, growthRate=4):
        super(MatrixRain, self).__init__(led)
        self._colors = colors
        self._tail = tail
        self._drops = [[] for x in range(self._led.width)]
        self._growthRate = growthRate
       
    def _drawDrop(self, x, y, color):
        for i in range(self._tail):
            if y-i >= 0 and y-i < self._led.height:
                level = 255 - ((255/self._tail)*i)
                self._led.set(x, y-i, colors.color_scale(color, level))

    def step(self, amt = 1):
        self._led.all_off()

        for i in range(self._growthRate):
            newDrop = random.randint(0, self._led.width - 1)
            cInt = random.randint(0, len(self._colors) - 1)
            self._drops[newDrop].append((0, self._colors[cInt]));

        for x in range(self._led.width):
            col = self._drops[x]
            if len(col) > 0:
                removals = []
                for y in range(len(col)):
                    drop = col[y]
                    if drop[0] < self._led.height:
                        self._drawDrop(x, drop[0], drop[1])
                    if drop[0] - (self._tail - 1) < self._led.height:
                        drop = (drop[0] + 1, drop[1])
                        self._drops[x][y] = drop
                    else:
                        removals.append(drop)
                for r in removals:
                    self._drops[x].remove(r)
                      
        self._step = 0

class MatrixRainBow(BaseMatrixAnim):

    def __init__(self, led, tail=4, growthRate=4):
        super(MatrixRainBow, self).__init__(led)
        self._tail = tail
        self._drops = [[] for x in range(self._led.width)]
        self._growthRate = growthRate
       
    def _drawDrop(self, x, y, color):
        for i in range(self._tail):
            if y-i >= 0 and y-i < self._led.height:
                level = 255 - ((255/self._tail)*i)
                self._led.set(x, y-i, colors.color_scale(color, level))

    def step(self, amt = 1):
        self._led.all_off()

        for i in range(self._growthRate):
            newDrop = random.randint(0, self._led.width - 1)
            self._drops[newDrop].append(0);

        for x in range(self._led.width):
            col = self._drops[x]
            if len(col) > 0:
                removals = []
                for y in range(len(col)):
                    drop = col[y]
                    if drop < self._led.height:
                        self._drawDrop(x, drop, colors.hue2rgb(drop * (255/self._led.height)))
                    if drop - (self._tail - 1) < self._led.height:
                        drop = drop + 1
                        self._drops[x][y] = drop
                    else:
                        removals.append(drop)
                for r in removals:
                    self._drops[x].remove(r)
                      
        self._step = 0

class SpiningTriangle(BaseMatrixAnim):
    def __init__(self, led, cx, cy, radius):
        super(SpiningTriangle, self).__init__(led)
        self._cx = cx
        self._cy = cy
        self._radius = radius
        self._angles = (0, 120, 240)

    def _stepAngle(self, a, step):
        a += step
        if a >= 360:
            a -= 360
        elif a < 0:
            a += 360
        return a

    def __stepAngles(self, a, step):
        return (self._stepAngle(a[0], step),self._stepAngle(a[1], step), self._stepAngle(a[2], step),)

    def step(self, amt = 1):
        self._led.all_off()
        a = pointOnCircle(self._cx, self._cy, self._radius, self._angles[0])
        b = pointOnCircle(self._cx, self._cy, self._radius, self._angles[1])
        c = pointOnCircle(self._cx, self._cy, self._radius, self._angles[2])

        color = colors.hue2rgb_360(self._angles[0])

        self._led.drawLine(a[0], a[1], b[0], b[1], color)
        self._led.drawLine(b[0], b[1], c[0], c[1], color)
        self._led.drawLine(c[0], c[1], a[0], a[1], color)

        self._angles = self.__stepAngles(self._angles, amt)

class ScrollText(BaseMatrixAnim):

    def __init__(self, led, text, xPos = 0, yPos = 0, color = colors.White, bgcolor = colors.Off, size = 1):
        super(ScrollText, self).__init__(led)
        self.bgcolor = bgcolor
        self.color = color
        self._text = text
        self.xPos = xPos
        self.yPos = yPos
        self._size = size
        self._strW = len(text)*6*size
       
    def step(self, amt = 1):
        self._led.all_off()
        self._led.drawText(self._text, self.xPos, self.yPos, color = self.color, bg = self.bgcolor, size = self._size)
        self.xPos -= amt
        if self.xPos + self._strW <= 0:
            self.xPos = self.startX + self.width - 1
            self.animComplete = True
                      
        self._step = 0

class BounceText(BaseMatrixAnim):

    def __init__(self, led, text, xPos = 0, yPos = 0, buffer = 0, color = colors.White, bgcolor = colors.Off, size = 1):
        super(BounceText, self).__init__(led)
        self.color = color
        self.bgcolor = bgcolor
        self._text = text
        self.xPos = xPos
        self.yPos = yPos
        self._size = size
        self._strW = len(text)*6*size
        self._dir = -1
        self._buffer = buffer
       
    def step(self, amt = 1):
        self._led.all_off()
        self._led.drawText(self._text, self.xPos, self.yPos, color = self.color, bg = self.bgcolor, size = self._size)

        if self._strW < self.width:
            if self.xPos <= 0 + self._buffer and self._dir == -1:
                self._dir = 1
            elif self.xPos + self._strW > self.width - self._buffer  and self._dir == 1:
                self._dir = -1
                self.animComplete = True
        else:
            if self.xPos + self._strW <= self.width - self._buffer  and self._dir == -1:
                self._dir = 1
            elif self.xPos >= 0 + self._buffer and self._dir == 1:
                self._dir = -1
                self.animComplete = True

        self.xPos += amt * self._dir
                      
        self._step = 0