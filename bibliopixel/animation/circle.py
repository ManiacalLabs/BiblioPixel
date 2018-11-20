from . animation import Animation
from .. layout import circle
from .. util import deprecated


class Circle(Animation):
    LAYOUT_CLASS = circle.Circle
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
