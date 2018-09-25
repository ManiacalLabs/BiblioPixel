import unittest
from fractions import Fraction

from bibliopixel.util.colors import palettes
from bibliopixel.util.colors.classic import Black, White, Red, Green, Blue


class PalettesTest(unittest.TestCase):
    def test_empty(self):
        self.assertIs(palettes.get('no such name'), None)

    def test_simple(self):
        p = palettes.get('flag')

        self.assertEqual(p[0], Red)
        self.assertEqual(p[1], White)
        self.assertEqual(p[2], Blue)

        self.assertEqual(p.get(0), Red)

        self.assertEqual(p.get(0.99), Red)
        self.assertEqual(p.get(1), White)

        self.assertEqual(p.get(1.99), White)
        self.assertEqual(p.get(2), Blue)

        self.assertEqual(p.get(2.99), Blue)
        self.assertEqual(p.get(3), Red)
