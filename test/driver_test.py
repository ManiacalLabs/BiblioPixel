import unittest

from bibliopixel import gamma
from bibliopixel.drivers.driver_base import DriverBase, ChannelOrder
from bibliopixel.drivers.APA102 import DriverAPA102
from bibliopixel.drivers.LPD8806 import DriverLPD8806
from bibliopixel.drivers.WS2801 import DriverWS2801
from bibliopixel.drivers.spi_driver_base import SpiDummyInterface

from bibliopixel import timedata


def mock_open(self, fname, perm='r'):
    pass


class DriverTest(unittest.TestCase):
    COLORS_PY = [(0, 0, 0),
                 (1, 8, 64),
                 (2, 16, 128),
                 (3, 24, 192)]

    COLORS_TD = timedata.ColorList255(COLORS_PY)

    ALL_COLORS = COLORS_PY, COLORS_TD

    SPD = dict(interface=SpiDummyInterface)

    def do_test(self, driver, colors, expected):
        driver.set_colors(colors, 0)
        driver._render()
        self.assertEqual(list(driver._buf), expected)

    def do_both_tests(self, driver, expected):
        for c in self.ALL_COLORS:
            self.do_test(driver, c, expected)

    def test_trivial(self):
        driver = DriverBase(num=4)
        for i in range(len(driver._buf)):
            driver._buf[i] = 23  # randomize
        self.assertTrue(all(driver._buf))
        driver.set_colors([(0, 0, 0)] * 4, 0)
        driver._render()
        self.assertFalse(any(driver._buf))  # It wrote zeroes!

    def test_simple(self):
        driver = DriverBase(num=4)
        expected = [0, 0, 0, 1, 8, 64, 2, 16, 128, 3, 24, 192]
        self.do_both_tests(driver, expected)

    def test_permute(self):
        driver = DriverBase(num=4, c_order=ChannelOrder.GRB)
        expected = [0, 0, 0, 8, 1, 64, 16, 2, 128, 24, 3, 192]
        self.do_both_tests(driver, expected)

    def test_permute2(self):
        driver = DriverBase(num=4, c_order=ChannelOrder.BRG)
        expected = [0, 0, 0, 64, 1, 8, 128, 2, 16, 192, 3, 24]
        self.do_both_tests(driver, expected)

    def test_gamma1(self):
        driver = DriverBase(num=4, gamma=gamma.LPD8806)
        expected = [128, 128, 128, 128, 128, 132, 128, 128, 151, 128, 128, 190]
        self.do_test(driver, self.COLORS_PY, expected)
        if timedata.enabled():
            # BP computations and TD computations are a little different.
            expected[-1] += 1
        self.do_test(driver, self.COLORS_TD, expected)

    def test_apa102(self):
        driver = DriverAPA102(num=4, **self.SPD)
        expected = [0, 0, 0, 0, 255, 0, 0, 0, 255, 1, 8, 64,
                    255, 2, 16, 128, 255, 3, 24, 192, 255, 0, 0, 0]
        self.do_test(driver, self.COLORS_PY, expected)
        # self.do_test(driver, self.COLORS_TD, expected) TODO

    def test_lpd8806(self):
        driver = DriverLPD8806(num=4, **self.SPD)
        expected = [
            128, 128, 128, 128, 128, 132, 128, 128, 151, 128, 128, 190, 0]
        self.do_test(driver, self.COLORS_PY, expected)
        if timedata.enabled():
            # BP computations and TD computations are a little different.
            expected[-2] += 1
        self.do_test(driver, self.COLORS_TD, expected)

    def test_ws2801(self):
        driver = DriverWS2801(num=4, **self.SPD)
        expected = [0, 0, 0, 0, 0, 8, 0, 0, 45, 0, 0, 125]
        self.do_both_tests(driver, expected)
