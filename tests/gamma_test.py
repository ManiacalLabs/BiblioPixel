import unittest

from bibliopixel import gamma

class GammaTest(unittest.TestCase):
    def table(self, **kwds):
        return gamma.Gamma(**kwds).table

    def test_compatibility(self):
        self.assertEqual(self.table(offset=0.5), gamma.APA102)
        self.assertEqual(self.table(), gamma.WS2801)
        self.assertEqual(self.table(), gamma.SM16716)
        self.assertEqual(self.table(gamma=1 / 0.45), gamma.WS2812B)
        self.assertEqual(self.table(offset=0.5, lower_bound=128), gamma.LPD8806)
