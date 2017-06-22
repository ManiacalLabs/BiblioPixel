from . animation import BaseAnimation
from .. layout import Cube


class BaseCubeAnim(BaseAnimation):

    def __init__(self, layout):
        super().__init__(layout)
        if not isinstance(layout, Cube):  # pragma: no cover
            raise RuntimeError('Must use bibliopixel.layout.Cube with ' +
                               'Cube Animations!')

        self.x, self.y, self.z = layout.x, layout.y, layout.z
