import unittest
from bibliopixel.layout import Strip
from bibliopixel.util import colors


class MockDriver:
    def __init__(self, numLEDs):
        self.numLEDs = numLEDs
        self._calls = []

    def __getattr__(self, name):
        return lambda *a, **k: self._calls.append((name, a, k))


class LayoutTest(unittest.TestCase):
    def test_set_colors(self):
        strip = Strip(MockDriver(4))
        strip.set(0, 'red'),
        strip.set(1, colors.Green)
        strip.set(2, 'hot pink')
        expected = [(255, 0, 0), (0, 255, 0), (255, 105, 180), (0, 0, 0)]
        self.assertEquals(expected, strip.color_list)
