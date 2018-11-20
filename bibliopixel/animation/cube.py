from . animation import Animation
from .. layout import cube


class Cube(Animation):
    LAYOUT_CLASS = cube.Cube
    LAYOUT_ARGS = 'x', 'y', 'z'

    def __init__(self, layout, **kwds):
        super().__init__(layout, **kwds)
        self.x, self.y, self.z = layout.x, layout.y, layout.z


from .. util import deprecated
if deprecated.allowed():
    BaseCubeAnim = Cube
