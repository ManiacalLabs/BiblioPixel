from . animation import Animation
from .. layout import Circle


class Circle(Animation):

    def __init__(self, layout, **kwds):
        super().__init__(layout, **kwds)

        if not isinstance(layout, Circle):
            raise RuntimeError('Must use bibliopixel.layout.Circle with ' +
                               'Circle Animations!')

        self.rings = layout.rings
        self.ringCount = layout.ringCount
        self.lastRing = layout.lastRing
        self.ringSteps = layout.ringSteps


# DEPRECATED
BaseCircleAnim = Circle
