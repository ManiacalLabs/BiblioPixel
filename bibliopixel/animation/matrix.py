from . animation import BaseAnimation
from .. layout import Matrix


class BaseMatrixAnim(BaseAnimation):

    def __init__(self, layout, width=0, height=0, startX=0, startY=0):
        super().__init__(layout)
        if not isinstance(layout, Matrix):  # pragma: no cover
            raise RuntimeError('Must use bibliopixel.layout.Matrix with ' +
                               'Matrix Animations!')

        self.width = width or layout.width
        self.height = height or layout.height

        self.startX = startX
        self.startY = startY
