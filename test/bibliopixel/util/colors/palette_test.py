import unittest
from fractions import Fraction

from bibliopixel.util.colors.palette import Palette
from bibliopixel.util.colors.classic import Black, White, Red, Green, Blue
from bibliopixel.util import log


class PaletteTest(unittest.TestCase):
    def test_empty(self):
        p = Palette()
        self.assertEqual(p[0], Black)
        self.assertEqual(p(), Black)
        self.assertEqual(p(1), Black)

    def test_single(self):
        p = Palette([Red])
        self.assertEqual(p[0], Red)
        self.assertEqual(p(), Red)
        self.assertEqual(p(1), Red)

    def test_get(self):
        p = Palette([Red, Green, Blue], continuous=True)
        result = [p(-1 + Fraction(i) / 2) for i in range(12)]
        expected = [
            (0, 170, 85),
            (0, 85, 170),
            (255, 0, 0),
            (170, 85, 0),
            (85, 170, 0),
            (0, 255, 0),
            (0, 170, 85),
            (0, 85, 170),
            (255, 0, 0),
            (170, 85, 0),
            (85, 170, 0),
            (0, 255, 0)]
        self.assertEqual(result, expected)

    def test_get_serpentine(self):
        p = Palette([Red, Green, Blue], serpentine=True, continuous=True)
        result = [p(-1 + Fraction(i) / 2) for i in range(12)]
        expected = [
            (85, 170, 0),
            (170, 85, 0),
            (255, 0, 0),
            (170, 85, 0),
            (85, 170, 0),
            (0, 255, 0),
            (0, 170, 85),
            (0, 85, 170),
            (0, 0, 255),
            (0, 85, 170),
            (0, 170, 85),
            (0, 255, 0)
        ]
        self.assertEqual(result, expected)

    def test_double(self):
        p = Palette([Red, Green], continuous=True)

        self.assertEqual(p[0], Red)
        self.assertEqual(p[1], Green)

        result = [p(-1 + Fraction(i) / 3) for i in range(12)]
        expected = [
            (127.5, 127.5, 0),
            (85, 170, 0),
            (42.5, 212.5, 0),
            (255, 0, 0),
            (212.5, 42.5, 0),
            (170, 85, 0),
            (127.5, 127.5, 0),
            (85, 170, 0),
            (42.5, 212.5, 0),
            (255, 0, 0),
            (212.5, 42.5, 0),
            (170, 85, 0)
        ]
        self.assertEqual(result, expected)

    def test_double_serpentine(self):
        p = Palette([Red, Green], serpentine=True, continuous=True)

        result = [p(-1 + Fraction(i) / 3) for i in range(12)]
        expected = [
            (127.5, 127.5, 0.0),
            (170.0, 85.0, 0.0),
            (212.5, 42.5, 0.0),
            (255.0, 0.0, 0.0),
            (212.5, 42.5, 0.0),
            (170.0, 85.0, 0.0),
            (127.5, 127.5, 0.0),
            (85.0, 170.0, 0.0),
            (42.5, 212.5, 0.0),
            (0.0, 255.0, 0.0),
            (42.5, 212.5, 0.0),
            (85.0, 170.0, 0.0)
        ]
        self.assertEqual(result, expected)

    def test_discontinuous(self):
        colors = [Red, Green, Blue, White]
        p = Palette(colors)

        result = [p(Fraction(i) / 2) for i in range(10)]
        expected = [Red, Red, Green, Green, Blue, Blue, White, White, Red, Red]

        self.assertEqual(expected, result)

    def test_discontinuous_serpentine(self):
        colors = [Red, Green, Blue, White]
        p = Palette(colors, serpentine=True)
        self.assertEqual(Green, p(7))

        self.assertEqual(Red, p(0))
        self.assertEqual(Green, p(1))
        self.assertEqual(Blue, p(2))
        self.assertEqual(White, p(3))
        self.assertEqual(Blue, p(4))
        self.assertEqual(Green, p(5))
        self.assertEqual(Red, p(6))
        self.assertEqual(Green, p(7))
        self.assertEqual(Blue, p(8))

        self.assertEqual(Red, p(0.1))
        self.assertEqual(Green, p(1.9))

    def test_continuous(self):
        colors = [Red, Green, Blue, White]
        p = Palette(colors, continuous=True)
        result = [p(-1 + Fraction(i) / 3) for i in range(16)]

        expected = [
            (63.75, 63.75, 255.0),
            (127.5, 127.5, 255.0),
            (191.25, 191.25, 255.0),
            (255.0, 0.0, 0.0),
            (191.25, 63.75, 0.0),
            (127.5, 127.5, 0.0),
            (63.75, 191.25, 0.0),
            (0.0, 255.0, 0.0),
            (0.0, 191.25, 63.75),
            (0.0, 127.5, 127.5),
            (0.0, 63.75, 191.25),
            (0.0, 0.0, 255.0),
            (63.75, 63.75, 255.0),
            (127.5, 127.5, 255.0),
            (191.25, 191.25, 255.0),
            (255.0, 0.0, 0.0),
        ]
        self.assertEqual(expected, result)

    def test_continuous_serpentine(self):
        colors = [Red, Green, Blue, White]
        p = Palette(colors, serpentine=True, continuous=True)
        result = [p(-1 + Fraction(i) / 3) for i in range(15)]

        expected = [
            (63.75, 191.25, 0.0),
            (127.5, 127.5, 0.0),
            (191.25, 63.75, 0.0),
            (255.0, 0.0, 0.0),
            (191.25, 63.75, 0.0),
            (127.5, 127.5, 0.0),
            (63.75, 191.25, 0.0),
            (0.0, 255.0, 0.0),
            (0.0, 191.25, 63.75),
            (0.0, 127.5, 127.5),
            (0.0, 63.75, 191.25),
            (0.0, 0.0, 255.0),
            (63.75, 63.75, 255.0),
            (127.5, 127.5, 255.0),
            (191.25, 191.25, 255.0)
        ]
        self.assertEqual(expected, result)

    def test_scale(self):
        colors = [Red, Green, Blue, White]
        p = Palette(colors, continuous=False, serpentine=True, scale=3)

        result = [p(Fraction(2 * i) / 9) for i in range(25)]
        expected = [
            Red, Red, Green, Blue, Blue, White, Blue, Green,
            Red, Red, Red, Green, Blue, Blue, White, Blue,
            Green, Red, Red, Red, Green, Blue, Blue, White,
            Blue]

        self.assertEqual(expected, result)

    def _print_result(self, result):
        result2 = [tuple(float(i) for i in c) for c in result]
        log.printer('', *result2, sep=',\n            ')

    def test_autoscale(self):
        colors = [Red, Green, Blue, White]
        p = Palette(colors, autoscale=True)

        expected = [Red, Red, Green, Green, Blue, Blue, White, White, Red, Red]
        result = [p(Fraction(i) / 2) for i in range(10)]
        self.assertEqual(expected, result)

        p.length = 256
        result = [p(32 * i) for i in range(10)]
        self.assertEqual(expected, result)

    def test_equality(self):
        colors = [Red, Green, Blue, White]
        p = Palette(colors, autoscale=True)
        q = Palette(colors, autoscale=True)

        self.assertEqual(p, q)
        self.assertFalse(p != q)

        r = Palette(colors)
        self.assertNotEqual(p, r)
        self.assertFalse(p == r)

        s = Palette(colors, serpentine=True)
        t = Palette(colors[:3], serpentine=True)
        self.assertNotEqual(s, t)
