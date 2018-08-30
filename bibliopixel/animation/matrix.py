from . animation import Animation
from .. layout import Matrix


class BaseMatrixAnim(Animation):
    LAYOUT_CLASS = Matrix
    LAYOUT_ARGS = 'width', 'height'

    def __init__(self, layout, width=0, height=0, **kwds):
        super().__init__(layout, **kwds)
        self.width = width or layout.width
        self.height = height or layout.height
