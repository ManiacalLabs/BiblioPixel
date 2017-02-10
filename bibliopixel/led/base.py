import time

from .. import colors, data_maker, util


class LEDBase(object):

    def __init__(self, drivers, threadedUpdate, masterBrightness,
                 maker=data_maker.MAKER):
        """Base LED class. Use LEDStrip or LEDMatrix instead!"""
        self.drivers = drivers if isinstance(drivers, list) else [drivers]

        if not hasattr(self, 'numLEDs'):
            self.numLEDs = sum(d.numLEDs for d in self.drivers)

        # This buffer will always be the same list - i.e. is guaranteed to only
        # be changed by list surgery, never assignment.
        self._colors = maker.color_list(self.numLEDs)

        pos = 0
        for d in self.drivers:
            d.set_colors(self._colors, pos)
            pos += d.numLEDs

        self.masterBrightness = 255

        self._frameGenTime = 0
        self._frameTotalTime = None

        self._threadedUpdate = threadedUpdate

        if self._threadedUpdate:
            self._updateThread = util.UpdateThread(self.drivers)
            self._updateThread.start()

        self._waitingBrightness = False
        self._waitingBrightnessValue = None
        self._threadedAnim = False

        self.set_brightness(masterBrightness)

    def set_layout(self, layout):
        for d in self.drivers:
            d.set_layout(layout)

    def update(self):
        """DEPRECATED - use self.push_to_driver()"""
        return self.push_to_driver()

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

    def get_layout(self):
        result = []
        for x in range(len(self.numLEDs)):
            result.append([x, 0, 0])
        return result

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
                          "Expected: {} bytes / Received: {} bytes"
                          .format(len(self._colors), len(buf)))
        self._colors[:] = buf

    def setBuffer(self, buf):
        """DEPRECATED!"""
        # https://stackoverflow.com/questions/1624883
        self.set_colors(buf=list(zip(*(iter(buf),) * 3)))

    # Set the master brightness for the LEDs 0 - 255
    def _do_set_brightness(self, bright):
        self.waitForUpdate()
        result = True
        for d in self.drivers:
            if not d.set_brightness(bright):
                result = False
                break

        # all or nothing, set them all back if False
        if not result:
            for d in self.drivers:
                d.set_brightness(255)
            self.masterBrightness = bright
        else:
            self.masterBrightness = 255

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
