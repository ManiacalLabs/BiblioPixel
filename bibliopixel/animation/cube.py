from . animation import BaseAnimation
from .. led import Cube


class BaseCubeAnim(BaseAnimation):

    def __init__(self, led):
        super().__init__(led)
        if not isinstance(led, Cube):  # pragma: no cover
            raise RuntimeError("Must use Cube with Matrix Animations!")

        self.x, self.y, self.z = led.x, led.y, led.z
