from . animation import Animation
from .. layout import Circle as CircleLayout
from .. util import deprecated


class Circle(Animation):
    LAYOUT_CLASS = CircleLayout
    LAYOUT_ARGS = 'rings',

    def __init__(self, layout, **kwds):
        super().__init__(layout, **kwds)
        self.rings = layout.rings
        self.ringCount = layout.ringCount
        if deprecated.allowed():  # pragma: no cover
            self.lastRing = layout.lastRing
        self.ringSteps = layout.ringSteps


if deprecated.allowed():  # pragma: no cover
    BaseCircleAnim = Circle
