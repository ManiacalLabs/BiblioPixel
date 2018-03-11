from . animation import Animation
from .. layout import Circle as CircleLayout


class Circle(Animation):

    def __init__(self, layout, **kwds):
        super().__init__(layout, **kwds)

        if not isinstance(layout, CircleLayout):
            raise RuntimeError(
                'Must use %s with Circle animations, not %s' %
                CircleLayout, type(layout))

        self.rings = layout.rings
        self.ringCount = layout.ringCount
        self.lastRing = layout.lastRing
        self.ringSteps = layout.ringSteps


from .. util import deprecated
if deprecated.allowed():
    BaseCircleAnim = Circle
