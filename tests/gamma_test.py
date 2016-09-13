import unittest

from bibliopixel import gamma

class GammaTest(unittest.TestCase):
    def test_lpd8806(self):
        self.assertEqual(tuple(gamma.NEW_LPD8806), gamma.NEWER_LPD8806)
