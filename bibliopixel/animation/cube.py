from . animation import Animation
from .. layout import Cube


class BaseCubeAnim(Animation):
    LAYOUT_CLASS = Cube
    LAYOUT_ARGS = 'x', 'y', 'z'

    def __init__(self, layout, **kwds):
        super().__init__(layout, **kwds)
        self.x, self.y, self.z = layout.x, layout.y, layout.z
