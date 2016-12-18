from . base import BaseAnimation
from .. led import LEDStrip


class BaseStripAnim(BaseAnimation):

    def __init__(self, led, start=0, end=-1):
        super().__init__(led)

        if not isinstance(led, LEDStrip):
            raise RuntimeError("Must use LEDStrip with Strip Animations!")

        self._start = max(start, 0)
        self._end = end
        if self._end < 0 or self._end >= self._led.numLEDs:
            self._end = self._led.numLEDs - 1

        self._size = self._end - self._start + 1
