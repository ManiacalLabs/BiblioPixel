import unittest

from bibliopixel.util import colors
COLORS = 'red', 'white', 'magenta', 'lime green', '(0, 1, 2)'


class NamesTest(unittest.TestCase):
    def test_round_trip(self):
        for name in COLORS:
            color = colors.name_to_color(name)
            name2 = colors.color_to_name(color)
            self.assertEqual(name, name2)

    def test_to_color(self):
        for name in COLORS:
            color1 = colors.name_to_color(name)
            color2 = colors.to_color(name)
            color3 = colors.to_color(color2)
            self.assertEqual(color1, color2)
            self.assertEqual(color2, color3)

        self.assertEqual(colors.to_color(0), colors.COLORS.black)
        self.assertEqual(colors.to_color([255]), colors.COLORS.white)
        self.assertEqual(colors.to_color((255, 0)), colors.COLORS.red)

    def test_name_to_color_error(self):
        colors.name_to_color('red')
        with self.assertRaises(ValueError):
            colors.name_to_color(3)
        with self.assertRaises(ValueError):
            colors.name_to_color('xxx')
        with self.assertRaises(ValueError):
            colors.name_to_color((1, 2, 3))

    def test_color_to_name_error(self):
        with self.assertRaises(ValueError):
            colors.color_to_name('red')
        with self.assertRaises(ValueError):
            colors.color_to_name(3)
        with self.assertRaises(ValueError):
            colors.color_to_name('xxx')
        colors.color_to_name((1, 2, 3))
