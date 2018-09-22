import unittest
from bibliopixel.layout import Strip
from bibliopixel.util.colors import COLORS

RED = COLORS.Red
GREEN = COLORS.Green
BLACK = COLORS.Black
HOT_PINK = COLORS['hot pink']


class MockDriver:
    def __init__(self, numLEDs):
        self.numLEDs = numLEDs
        self._calls = []

    def __getattr__(self, name):
        return lambda *a, **k: self._calls.append((name, a, k))


class LayoutTest(unittest.TestCase):
    def test_set_individual_colors(self):
        strip = Strip(MockDriver(4))
        strip.set(0, 'red'),
        strip.set(1, GREEN)
        strip.set(2, 'hot pink')
        expected = [RED, GREEN, HOT_PINK, BLACK]
        self.assertEqual(expected, strip.color_list)

    def test_set_color(self):
        strip = Strip(MockDriver(4))
        strip.color_list = RED, GREEN, HOT_PINK
        expected = [RED, GREEN, HOT_PINK, BLACK]
        self.assertEqual(expected, strip.color_list)

    def test_set_linear_color(self):
        strip = Strip(MockDriver(4))
        strip.color_list = RED + GREEN + HOT_PINK
        expected = [RED, GREEN, HOT_PINK, BLACK]
        self.assertEqual(expected, strip.color_list)

    def test_set_too_much_color(self):
        strip = Strip(MockDriver(4))
        strip.color_list = RED + GREEN + HOT_PINK + GREEN + HOT_PINK
        expected = [RED, GREEN, HOT_PINK, GREEN]
        self.assertEqual(expected, strip.color_list)

    def test_set_partial_color(self):
        strip = Strip(MockDriver(4))
        strip.color_list = (RED + GREEN + HOT_PINK + GREEN)[:-1]
        expected = [RED, GREEN, HOT_PINK, BLACK]
        self.assertEqual(expected, strip.color_list)

    def test_set_offset(self):
        strip = Strip(MockDriver(4))
        strip.set_color_list(RED + GREEN, 2)
        expected = [BLACK, BLACK, RED, GREEN]
        self.assertEqual(expected, strip.color_list)

    def test_clone(self):
        strip = Strip(MockDriver(4))
        clone = strip.clone()
        clone.set(1, RED)
        self.assertEqual(clone.get(1), RED)
        self.assertEqual(strip.get(1), BLACK)
