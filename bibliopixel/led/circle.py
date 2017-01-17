from . base import LEDBase
from .. import color_list


class LEDCircle(LEDBase):

    def __init__(self, drivers, rings, maxAngleDiff=0, rotation=0, threadedUpdate=False, masterBrightness=255, maker=color_list.MAKER):
        super().__init__(drivers, threadedUpdate, masterBrightness, maker)
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
