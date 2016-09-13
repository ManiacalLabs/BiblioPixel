import unittest

from bibliopixel import gamma
from bibliopixel.drivers.driver_base import DriverBase, ChannelOrder
from bibliopixel.drivers.APA102 import DriverAPA102
from bibliopixel.drivers.LPD8806 import DriverLPD8806
from bibliopixel.drivers.WS2801 import DriverWS2801


def mock_open(self, fname, perm='r'):
    pass #

class DriverTest(unittest.TestCase):
    COLORS = [(0, 0, 0),
              (1, 8, 64),
              (2, 16, 128),
              (3, 24, 192)]

    SPD = dict(use_py_spi=False, open=mock_open)

    def test_trivial(self):
        driver = DriverBase(num=4)
        for i in range(len(driver._buf)):
           driver._buf[i] = 23  # randomize
        self.assertTrue(all(driver._buf))
        driver._render([(0, 0, 0)] * 4, 0)
        self.assertFalse(any(driver._buf))  # It wrote zeroes!

    def test_simple(self):
        driver = DriverBase(num=4)
        driver._render(self.COLORS, 0)
        self.assertEqual(
            list(driver._buf), [0, 0, 0, 1, 8, 64, 2, 16, 128, 3, 24, 192])

    def test_permute(self):
        driver = DriverBase(num=4, c_order=ChannelOrder.GRB)
        driver._render(self.COLORS, 0)
        self.assertEqual(
            list(driver._buf), [0, 0, 0, 8, 1, 64, 16, 2, 128, 24, 3, 192])

        driver = DriverBase(num=4, c_order=ChannelOrder.BRG)
        driver._render(self.COLORS, 0)
        self.assertEqual(
            list(driver._buf), [0, 0, 0, 64, 1, 8, 128, 2, 16, 192, 3, 24])

    def test_gamma(self):
        driver = DriverBase(num=4, gamma=gamma.OLD_LPD8806)
        driver._render(self.COLORS, 0)
        self.assertEqual(
            list(driver._buf), [0, 0, 0, 0, 0, 8, 0, 0, 46, 0, 1, 125])

        driver = DriverBase(num=4, c_order=ChannelOrder.RGB,
                            gamma=gamma.OLD_LPD8806)
        driver._render(self.COLORS, 0)
        self.assertEqual(
            list(driver._buf), [0, 0, 0, 0, 0, 8, 0, 0, 46, 0, 1, 125])

    def test_apa102(self):
        driver = DriverAPA102(num=4, **self.SPD)
        driver._render(self.COLORS, 0)
        self.assertEqual(
            list(driver._buf),
            [0, 0, 0, 0, 255, 0, 0, 0, 255, 1, 8, 64,
             255, 2, 16, 128, 255, 3, 24, 192, 255, 0, 0, 0])

    def test_lpd8806(self):
        driver = DriverLPD8806(num=4, **self.SPD)
        driver._render(self.COLORS, 0)
        self.assertEqual(
            list(driver._buf),
            [128, 128, 128, 128, 128, 132,
             128, 128, 151, 128, 128, 190, 0])

    def test_ws2801(self):
        driver = DriverWS2801(num=4, **self.SPD)
        driver._render(self.COLORS, 0)
        self.assertEqual(
            list(driver._buf), [0, 0, 0, 0, 0, 8, 0, 0, 45, 0, 0, 125])
