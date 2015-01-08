from bibliopixel import LEDStrip
import bibliopixel.colors as colors
from bibliopixel.animation import BaseStripAnim

import math
import time
import random

class Rainbow(BaseStripAnim):
    """Generate rainbow distributed over 256 pixels.
       If you want the full rainbow to fit in the number of pixels you
       are using, use RainbowCycle instead 
    """

    def __init__(self, led, start=0, end=-1):
        super(Rainbow, self).__init__(led, start, end)

    def step(self, amt = 1):
        for i in range(self._size):
            h = (i + self._step) % 255
            self._led.set(self._start + i, colors.hue2rgb_rainbow(h))

        self._step += amt
        overflow = self._step - 256
        if overflow >= 0:
            self._step = overflow

class RainbowCycle(BaseStripAnim):
    """Generate rainbow wheel equally distributed over strip."""

    def __init__(self, led, start=0, end=-1):
        super(RainbowCycle, self).__init__(led, start, end)

    def step(self, amt = 1):
        for i in range(self._size):
            #color = (i * (384 / self._size) + self._step) % 384
            #c = colors.wheel_helper(i, self._size, self._step)
            c = colors.hue_helper(i, self._size, self._step)
            self._led.set(self._start + i, c)

        self._step += amt
        overflow = self._step - 256
        if overflow >= 0:
            self._step = overflow

class ColorPattern(BaseStripAnim):
    """Fill the dots progressively along the strip with alternating colors."""

    def __init__(self, led, colors, width, dir = True, start=0, end=-1):
        super(ColorPattern, self).__init__(led, start, end)
        self._colors = colors
        self._colorCount = len(colors)
        self._width = width
        self._total_width = self._width * self._colorCount;
        self._dir = dir

    def step(self, amt = 1):
        for i in range(self._size):
            cIndex = ((i+self._step) % self._total_width) / self._width;
            self._led.set(self._start + i, self._colors[cIndex])
        if self._dir:
            self._step += amt
            overflow = (self._start + self._step) - self._end
            if overflow >= 0:
                self._step = overflow
        else:
            self._step -= amt
            if self._step < 0:
                self._step = self._end + self._step

class ColorWipe(BaseStripAnim):
    """Fill the dots progressively along the strip."""

    def __init__(self, led, color, start=0, end=-1):
        super(ColorWipe, self).__init__(led, start, end)
        self._color = color

    def step(self, amt = 1):
        if self._step == 0:
            self._led.all_off()
        for i in range(amt):
            self._led.set(self._start + self._step - i, self._color)

        self._step += amt
        overflow = (self._start + self._step) - self._end
        if overflow >= 0:
            self._step = overflow

class ColorFade(BaseStripAnim):
    """Fill the dots progressively along the strip."""

    def wave_range(self, start, peak, step):
        main = [i for i in range(start, peak+1, step)]
        return main + [i for i in reversed(main[0:len(main)-1])]

    def __init__(self, led, colors, step = 5, start=0, end=-1):
        super(ColorFade, self).__init__(led, start, end)
        self._colors = colors
        self._levels = self.wave_range(30, 255, step)
        self._level_count = len(self._levels)
        self._color_count = len(colors)

    def step(self, amt = 1):
        if self._step > self._level_count * self._color_count:
            self._step = 0

        c_index = (self._step / self._level_count) % self._color_count
        l_index = (self._step % self._level_count)
        color = self._colors[c_index];
        self._led.fill(colors.color_scale(color, self._levels[l_index]), self._start, self._end)

        self._step += amt

class ColorChase(BaseStripAnim):
    """Chase one pixel down the strip."""

    def __init__(self, led, color, width=1, start=0, end=-1):
        super(ColorChase, self).__init__(led, start, end)
        self._color = color
        self._width = width

    def step(self, amt = 1):
        self._led.all_off() #because I am lazy

        for i in range(self._width):
            self._led.set(self._start + self._step + i, self._color)

        self._step += amt
        overflow = (self._start + self._step) - self._end
        if overflow >= 0:
            self._step = overflow

class PartyMode(BaseStripAnim):
    """Stobe Light Effect."""

    def __init__(self, led, colors, start=0, end=-1):
        super(PartyMode, self).__init__(led, start, end)
        self._colors = colors
        self._color_count = len(colors)

    def step(self, amt = 1):
        amt = 1 #anything other than 1 would be just plain silly
        if self._step > (self._color_count * 2) - 1:
            self._step = 0

        if self._step % 2 == 0:
            self._led.fill(self._colors[self._step / 2], self._start, self._end)
        else:
            self._led.all_off()

        self._step += amt

class FireFlies(BaseStripAnim):
    """Stobe Light Effect."""
    def __init__(self, led, colors, width = 1, count = 1, start=0, end=-1):
        super(FireFlies, self).__init__(led, start, end)
        self._colors = colors
        self._color_count = len(colors)
        self._width = width
        self._count = count

    def step(self, amt = 1):
        amt = 1 #anything other than 1 would be just plain silly
        if self._step > self._led.numLEDs:
            self._step = 0

        self._led.all_off();

        for i in range(self._count):
            pixel = random.randint(0, self._led.numLEDs - 1)
            color = self._colors[random.randint(0, self._color_count - 1)]

            for i in range(self._width):
                if pixel + i < self._led.numLEDs:
                    self._led.set(pixel + i, color)

        self._step += amt

class LarsonScanner(BaseStripAnim):
    """Larson scanner (i.e. Cylon Eye or K.I.T.T.)."""

    def __init__(self, led, color, tail=2, start=0, end=-1):
        super(LarsonScanner, self).__init__(led, start, end)
        self._color = color

        self._tail = tail + 1  # makes tail math later easier
        if self._tail >= self._size / 2:
            self._tail = (self._size / 2) - 1

        self._direction = -1
        self._last = 0
        self._fadeAmt = 256 / self._tail

    def step(self, amt = 1):
        self._led.all_off()

        self._last = self._start + self._step
        self._led.set(self._last, self._color)

        for i in range(self._tail):
            self._led.set(self._last - i, colors.color_scale(self._color, 255 - (self._fadeAmt * i)))
            self._led.set(self._last + i, colors.color_scale(self._color, 255 - (self._fadeAmt * i)))

        if self._start + self._step >= self._end:
            self._direction = -self._direction
        elif self._step <= 0:
            self._direction = -self._direction

        self._step += self._direction * amt

class LarsonRainbow(LarsonScanner):
    """Larson scanner (i.e. Cylon Eye or K.I.T.T.) but Rainbow."""

    def __init__(self, led, tail=2, start=0, end=-1):
        super(LarsonRainbow, self).__init__(
            led, colors.Off, tail, start, end)

    def step(self, amt = 1):
        self._color = colors.hue_helper(0, self._size, self._step)
        #self._color = colors.hue2rgb_rainbow((self._step * (256 / self._size)) % 256)

        super(LarsonRainbow, self).step(amt)

class Wave(BaseStripAnim):
    """Sine wave animation."""

    def __init__(self, led, color, cycles, start=0, end=-1):
        super(Wave, self).__init__(led, start, end)
        self._color = color
        self._cycles = cycles

    def step(self, amt = 1):
        for i in range(self._size):
            y = math.sin(
                math.pi *
                float(self._cycles) *
                float(self._step * i) /
                float(self._size))

            if y >= 0.0:
                # Peaks of sine wave are white
                y = 1.0 - y  # Translate Y to 0.0 (top) to 1.0 (center)
                r, g, b = self._color
                c2 = (int(255 - float(255 - r) * y), int(255 - float(255 - g) * y), int(255 - float(255 - b) * y))
            else:
                # Troughs of sine wave are black
                y += 1.0  # Translate Y to 0.0 (bottom) to 1.0 (center)
                r, g, b = self._color
                c2 = (int(float(r) * y),
                           int(float(g) * y),
                           int(float(b) * y))
            self._led.set(self._start + i, c2)

        self._step += amt

class WaveMove(BaseStripAnim):
    """Sine wave animation."""

    def __init__(self, led, color, cycles, start=0, end=-1):
        super(WaveMove, self).__init__(led, start, end)
        self._color = color
        self._cycles = cycles
        self._moveStep = 0

    def step(self, amt = 1):
        for i in range(self._size):
            y = math.sin(
                (math.pi *
                float(self._cycles) *
                float(i) /
                float(self._size)) 
                + self._moveStep)

            if y >= 0.0:
                # Peaks of sine wave are white
                y = 1.0 - y  # Translate Y to 0.0 (top) to 1.0 (center)
                r, g, b = self._color
                c2 = (int(255 - float(255 - r) * y), int(255 - float(255 - g) * y), int(255 - float(255 - b) * y))
            else:
                # Troughs of sine wave are black
                y += 1.0  # Translate Y to 0.0 (bottom) to 1.0 (center)
                r, g, b = self._color
                c2 = (int(float(r) * y),
                           int(float(g) * y),
                           int(float(b) * y))
            self._led.set(self._start + i, c2)

        self._step += amt
        self._moveStep += 1
        if(self._moveStep >= self._size):
            self._moveStep = 0

import time
class RGBClock(BaseStripAnim):
    """RGB Clock done with RGB LED strip(s)"""

    def __init__(self, led, hStart, hEnd, mStart, mEnd, sStart, sEnd):
        super(RGBClock, self).__init__(led, 0, -1)
        if hEnd < hStart:
            hEnd = hStart + 1
        if mEnd < mStart:
            mEnd = mStart + 1
        if sEnd < sStart:
            sEnd = sStart + 1
        self._hStart = hStart
        self._hEnd = hEnd
        self._mStart = mStart
        self._mEnd = mEnd
        self._sStart = sStart
        self._sEnd = sEnd
        

    def step(self, amt = 1):
        t = time.localtime()

        r, g, b = colors.hue2rgb_rainbow(t.tm_hour * (256/24))
        self._led.fillRGB(r,g,b,self._hStart,self._hEnd)

        r, g, b = colors.hue2rgb_rainbow(t.tm_min * (256/60))
        self._led.fillRGB(r,g,b,self._mStart,self._mEnd)

        r, g, b = colors.hue2rgb_rainbow(t.tm_sec * (256/60))
        self._led.fillRGB(r,g,b,self._sStart,self._sEnd)

        self._step = 0