from . animation import BaseAnimation
from .. layout import Matrix


class BaseMatrixAnim(BaseAnimation):

    def __init__(self, led, width=0, height=0, startX=0, startY=0):
        super().__init__(led)
        if not isinstance(led, Matrix):  # pragma: no cover
            raise RuntimeError("Must use Matrix with Matrix Animations!")

        self.width = width or led.width
        self.height = height or led.height

        self.startX = startX
        self.startY = startY
