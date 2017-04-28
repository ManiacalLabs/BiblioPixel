from . animation import BaseAnimation
from .. led import LEDCube


class BaseCubeAnim(BaseAnimation):

    def __init__(self, led):
        super().__init__(led)
        if not isinstance(led, LEDCube):  # pragma: no cover
            raise RuntimeError("Must use LEDCube with Matrix Animations!")

        self.x, self.y, self.z = led.x, led.y, led.z
