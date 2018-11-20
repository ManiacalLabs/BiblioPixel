import unittest

from bibliopixel.colors import COLORS, names
_COLORS = 'red', 'white', 'magenta', 'lime green', '(0, 1, 2)'


class NamesTest(unittest.TestCase):
    def test_round_trip(self):
        for name in _COLORS:
            color = names.name_to_color(name)
            name2 = names.color_to_name(color)
            self.assertEqual(name, name2)

    def test_to_color(self):
        for name in _COLORS:
            color1 = names.name_to_color(name)
            color2 = names.to_color(name)
            color3 = names.to_color(color2)
            self.assertEqual(color1, color2)
            self.assertEqual(color2, color3)

        self.assertEqual(names.to_color(0), COLORS.black)
        self.assertEqual(names.to_color([255]), COLORS.white)
        self.assertEqual(names.to_color((255, 0)), COLORS.red)

    def test_name_to_color_error(self):
        names.name_to_color('red')
        with self.assertRaises(ValueError):
            names.name_to_color(3)
        with self.assertRaises(ValueError):
            names.name_to_color('xxx')
        with self.assertRaises(ValueError):
            names.name_to_color((1, 2, 3))

    def test_color_to_name_error(self):
        with self.assertRaises(ValueError):
            names.color_to_name('red')
        with self.assertRaises(ValueError):
            names.color_to_name(3)
        with self.assertRaises(ValueError):
            names.color_to_name('xxx')
        names.color_to_name((1, 2, 3))
