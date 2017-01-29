import unittest

from bibliopixel import colors


class ArithmeticTest(unittest.TestCase):
    def test_color_blend(self):
        self.assertEqual(colors.color_blend(colors.Red, colors.Green),
                         (255, 255, 1))
        self.assertEqual(colors.color_blend(colors.Red, colors.White),
                         (255, 255, 255))
        self.assertEqual(colors.color_blend(colors.Red, colors.Black),
                         (255, 1, 1))

    def test_color_scale(self):
        self.assertEqual(colors.Green, (0, 255, 0))
        self.assertEqual(colors.color_scale(colors.Green, 256), (0, 255, 0))
        self.assertEqual(colors.color_scale(colors.Green, 255), (0, 254, 0))
        self.assertEqual(colors.color_scale(colors.Green, 128), (0, 127, 0))
        self.assertEqual(colors.color_scale(colors.Green, 0), (0, 0, 0))
