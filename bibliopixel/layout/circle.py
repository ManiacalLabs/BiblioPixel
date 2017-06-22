from . layout import Layout
from .. import data_maker
from . geometry.circle import (
    gen_circle, calc_ring_steps, calc_ring_pixel_count,
    pixel_positions_from_rings)


class Circle(Layout):

    def __init__(self, drivers, rings=[], pixels_per=None,
                 maxAngleDiff=0, rotation=0,
                 threadedUpdate=False, brightness=255, **kwargs):
        super().__init__(drivers, threadedUpdate, brightness,
                         maker=kwargs.get('maker', data_maker.MAKER))
        self.rings = rings
        self.maxAngleDiff = maxAngleDiff
        full_coords = False
        for r in self.rings:
            full_coords |= (len(r) > 2)

        if not full_coords:
            self.rings, self.ringSteps = gen_circle(
                rings=self.rings, pixels_per=pixels_per)
        else:
            self.ringSteps = calc_ring_steps(self.rings)

        self.ringCount = len(self.rings)
        self.lastRing = self.ringCount - 1

        self.set_pixel_positions(pixel_positions_from_rings(self.rings))

        num = calc_ring_pixel_count(self.rings)

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
        length = len(self.rings[ring]) - 1

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

        return self.rings[ring][offset]

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
                stop = len(r) - 1

            return [r[i] for i in range(start, stop + 1)]

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


# This is DEPRECATED
LEDCircle = Circle
