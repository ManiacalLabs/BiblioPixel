from . animation import BaseAnimation
from .. layout import Matrix


class BaseMatrixAnim(BaseAnimation):

    def __init__(self, layout, width=0, height=0, **kwds):
        super().__init__(layout, **kwds)
        if not isinstance(layout, Matrix):  # pragma: no cover
            raise RuntimeError('Must use bibliopixel.layout.Matrix with ' +
                               'Matrix Animations!')

        self.width = width or layout.width
        self.height = height or layout.height
