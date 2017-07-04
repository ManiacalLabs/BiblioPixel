import unittest

from bibliopixel import colors
from bibliopixel.colors import classic, names


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


class ClassicTest(unittest.TestCase):
    def test_classic(self):
        # Make sure that the classic and new color names are the same.
        cc = names.CLASSIC_COLORS
        jc = names.JUCE_COLORS
        for name, color in cc.items():
            self.assertEquals(color, jc.get(name, color), name)

        # Find all the dupes in classic colors.
        dupes = {}
        for k, v in cc.items():
            dupes.setdefault(v, []).append(k)

        dupes2 = {k: v for k, v in dupes.items() if len(v) > 1}
        self.assertEquals(set(dupes2), {
            (0, 0, 0), (255, 255, 255), (0, 255, 0), (255, 0, 255),
            (0, 255, 255)})

        # Now find which colors appear in classic but not in Juce.
        classics_add = set(cc.values()) - set(jc.values())
        self.assertEquals(classics_add,
                          {(169, 169, 169), (0, 128, 0),
                           (153, 102, 204), (204, 85, 51)})


class NamesTest(unittest.TestCase):
    def test_colors(self):
        self.assertEquals(names.COLORS.red, (255, 0, 0))
        self.assertEquals(names.COLORS.OFF, (0, 0, 0))
        self.assertEquals(names.COLORS['o n'], (255, 255, 255))
        self.assertEquals(names.COLORS((0, 0, 0)), 'black')
        self.assertEquals(names.COLORS((0x8a, 0x36, 0x0f)), 'burnt sienna')

    def test_toggle(self):
        self.assertEquals(names.toggle('red'), '(255, 0, 0)')
        self.assertEquals(names.toggle('(255, 0, 0)'), 'red')
        self.assertEquals(names.toggle('OFF'), '(0, 0, 0)')
        self.assertEquals(names.toggle('o n'), '(255, 255, 255)')
        self.assertEquals(names.toggle('(0, 0, 0)'), 'black')
        self.assertEquals(names.toggle('(0x8a, 0x36, 0x0f)'), 'burnt sienna')
