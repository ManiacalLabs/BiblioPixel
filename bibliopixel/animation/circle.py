from . animation import BaseAnimation
from .. led import Circle


class BaseCircleAnim(BaseAnimation):

    def __init__(self, led):
        super().__init__(led)

        if not isinstance(led, Circle):
            raise RuntimeError("Must use Circle with Circle Animations!")

        self.rings = led.rings
        self.ringCount = led.ringCount
        self.lastRing = led.lastRing
        self.ringSteps = led.ringSteps
