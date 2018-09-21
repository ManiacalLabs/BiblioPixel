import unittest
from fractions import Fraction

from bibliopixel.util.colors.palette import Palette
from bibliopixel.util.colors.classic import Black, White, Red, Green, Blue


class PaletteTest(unittest.TestCase):
    def test_empty(self):
        p = Palette()
        self.assertEqual(p[0], Black)
        self.assertEqual(p.interpolate(0), Black)
        self.assertEqual(p.interpolate(1), Black)

    def test_single(self):
        p = Palette([Red])
        self.assertEqual(p[0], Red)
        self.assertEqual(p.interpolate(0), Red)
        self.assertEqual(p.interpolate(1), Red)

    def test_double(self):
        p = Palette([Red, Green])
        self.assertEqual(p[0], Red)
        self.assertEqual(p[1], Green)

        self.assertEqual(p.interpolate(0), Red)
        self.assertEqual(p.interpolate(1), Red)

        p.serpentine = True
        self.assertEqual(p.interpolate(1), Green)

        one_third = Fraction(1, 3)
        self.assertEqual(p.interpolate(one_third),
                         (Fraction(170), Fraction(85), Fraction(0)))
        self.assertEqual(p.interpolate(1 - one_third),
                         (Fraction(85), Fraction(170), Fraction(0)))

    def test_discontinuous(self):
        colors = [Red, Green, Blue, White]
        p = Palette(colors, continuous=False)

        result = [p.interpolate(Fraction(i) / 8) for i in range(10)]
        expected = [Red, Red, Green, Green, Blue, Blue, White, White, Red, Red]

        self.assertEqual(expected, result)

    def test_discontinuous_serpentine(self):
        colors = [Red, Green, Blue, White]
        p = Palette(colors, continuous=False, serpentine=True)

        self.assertEqual(p.interpolate(Fraction(8) / 6), Blue)
        self.assertEqual(p.interpolate(1), White)

        result = [p.interpolate(Fraction(i) / 6) for i in range(25)]
        expected = [
            Red, Red, Green, Green, Blue, Blue,
            White, White, Blue, Blue, Green, Green,
            Red, Red, Green, Green, Blue, Blue,
            White, White, Blue, Blue, Green, Green,
            Red]

        self.assertEqual(expected, result)

    def test_continuous(self):
        colors = [Red, Green, Blue, White]
        p = Palette(colors)
        result = [p.interpolate(i / 8) for i in range(10)]
        expected = [
            (255.0, 0.0, 0.0),
            (159.375, 95.625, 0.0),
            (63.75, 191.25, 0.0),
            (0.0, 223.125, 31.875),
            (0.0, 127.5, 127.5),
            (0.0, 31.875, 223.125),
            (63.75, 63.75, 255.0),
            (159.375, 159.375, 255.0),
            (255.0, 0.0, 0.0),
            (159.375, 95.625, 0.0)]

        self.assertEqual(expected, result)

    def test_continuous_serpentine(self):
        colors = [Red, Green, Blue, White]
        p = Palette(colors, serpentine=True)
        result = [p.interpolate(i / 8) for i in range(10)]
        expected = [
            (255.0, 0.0, 0.0),
            (159.375, 95.625, 0.0),
            (63.75, 191.25, 0.0),
            (0.0, 223.125, 31.875),
            (0.0, 127.5, 127.5),
            (0.0, 31.875, 223.125),
            (63.75, 63.75, 255.0),
            (159.375, 159.375, 255.0),
            (255, 255, 255),
            (159.375, 159.375, 255.0)]

        self.assertEqual(expected, result)

    def test_scale(self):
        colors = [Red, Green, Blue, White]
        p = Palette(colors, continuous=False, serpentine=True, scale=3)

        result = [p.interpolate(Fraction(i) / 18) for i in range(25)]
        expected = [
            Red, Red, Green, Green, Blue, Blue,
            White, White, Blue, Blue, Green, Green,
            Red, Red, Green, Green, Blue, Blue,
            White, White, Blue, Blue, Green, Green,
            Red]

        self.assertEqual(expected, result)
