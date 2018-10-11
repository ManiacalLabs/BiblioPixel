import collections, unittest

from bibliopixel.util.colors import closest_colors

closest = closest_colors.closest_colors


class ClosestColorsTest(unittest.TestCase):
    def exhaustive(self, metric, start=32, skip=64, report=4):
        for color in closest_colors.all_colors(start, skip=skip):
            cl = closest(color, metric)
            if len(cl) >= report:
                yield color, cl

    def test_simple(self):
        self.assertEqual(closest((255, 0, 0)), ['red', 'red 1'])

    def test_far(self):
        c = closest((0, 0, 64), metric=closest_colors.taxicab)
        self.assertEqual(c, ['black', 'navy', 'none', 'off'])

        c = closest((64, 0, 0), metric=closest_colors.taxicab)
        self.assertEqual(c, ['black', 'maroon', 'none', 'off'])

    def test_euclidean(self):
        ex = list(self.exhaustive(closest_colors.euclidean))
        self.assertEqual(ex, [])

    def test_taxicab(self):
        ex = list(self.exhaustive(closest_colors.taxicab))
        self.assertEqual(ex, [])
