import unittest
from fractions import Fraction

from bibliopixel.colors import make, COLORS


class MakeTest(unittest.TestCase):
    def test_color(self):
        self.assertEqual(make.color('red'), COLORS.red)

    def test_split_colors1(self):
        test = 'red, green, [25, 81, 100], yellow'
        actual = list(make._split_colors(test))
        expected = ['red', 'green', '[25, 81, 100]', 'yellow']
        self.assertEqual(actual, expected)

    def test_split_colors2(self):
        test = '[12, 12, 12], red, green, [25, 81, 100], yellow, (3, 4, 5)'
        actual = list(make._split_colors(test))
        expected = ['[12, 12, 12]', 'red', 'green', '[25, 81, 100]',
                    'yellow', '(3, 4, 5)']
        self.assertEqual(actual, expected)

    def test_colors0(self):
        test = 'red, green, yellow'
        actual = list(make.colors(test))
        expected = [COLORS.red, COLORS.green, COLORS.yellow]
        self.assertEqual(actual, expected)

    def test_colors1(self):
        test = 'red, green, [25, 81, 100], yellow'
        actual = list(make.colors(test))
        expected = [COLORS.red, COLORS.green, (25, 81, 100), COLORS.yellow]
        self.assertEqual(actual, expected)

    def test_colors2(self):
        test = '[12, 12, 12], red, green, [25, 81, 100], yellow, (3, 4, 5)'
        actual = list(make.colors(test))
        expected = [(12, 12, 12), COLORS.red, COLORS.green, (25, 81, 100),
                    COLORS.yellow, (3, 4, 5)]
        self.assertEqual(actual, expected)
