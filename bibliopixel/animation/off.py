from . base import BaseAnimation


class OffAnim(BaseAnimation):
    """A trivial animation that turns all LEDs off."""

    def __init__(self, led, timeout=10):
        super().__init__(led)
        self._internalDelay = timeout * 1000.0

    def step(self, amt=1):
        self._led.all_off()
