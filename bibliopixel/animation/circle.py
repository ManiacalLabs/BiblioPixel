from . base import BaseAnimation
from .. led import LEDCircle


class BaseCircleAnim(BaseAnimation):

    def __init__(self, led):
        super().__init__(led)

        if not isinstance(led, LEDCircle):
            raise RuntimeError("Must use LEDCircle with Circle Animations!")

        self.rings = led.rings
        self.ringCount = led.ringCount
        self.lastRing = led.lastRing
        self.ringSteps = led.ringSteps
