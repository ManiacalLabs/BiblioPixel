from . animation import Animation
from .. layout import Strip


class BaseStripAnim(Animation):
    LAYOUT_CLASS = Strip
    LAYOUT_ARGS = 'num',

    def __init__(self, layout, start=0, end=-1, **kwds):
        super().__init__(layout, **kwds)

        self._start = max(start, 0)
        self._end = end
        if self._end < 0 or self._end >= self.layout.numLEDs:
            self._end = self.layout.numLEDs - 1

        self._size = self._end - self._start + 1
