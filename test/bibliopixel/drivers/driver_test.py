import unittest

from bibliopixel.util.colors import gamma
from bibliopixel.drivers.driver_base import DriverBase, ChannelOrder
from bibliopixel.drivers.SPI import SPI, SPI_INTERFACES
from bibliopixel.drivers.ledtype import LEDTYPE


class DriverTest(unittest.TestCase):
    COLORS = [(0, 0, 0),
              (1, 8, 64),
              (2, 16, 128),
              (3, 24, 192)]

    SPD = dict(interface=SPI_INTERFACES.DUMMY)

    def do_test(self, driver, expected):
        driver.set_colors(self.COLORS, 0)
        driver._render()
        self.assertEqual(list(driver._buf), expected)

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
        self.do_test(driver, expected)

    def test_permute(self):
        driver = DriverBase(num=4, c_order=ChannelOrder.GRB)
        expected = [0, 0, 0, 8, 1, 64, 16, 2, 128, 24, 3, 192]
        self.do_test(driver, expected)

    def test_permute2(self):
        driver = DriverBase(num=4, c_order=ChannelOrder.BRG)
        expected = [0, 0, 0, 64, 1, 8, 128, 2, 16, 192, 3, 24]
        self.do_test(driver, expected)

    def test_gamma1(self):
        driver = DriverBase(num=4, gamma=gamma.LPD8806)
        expected = [128, 128, 128, 128, 128, 132, 128, 128, 151, 128, 128, 190]
        self.do_test(driver, expected)

    def test_apa102(self):
        driver = SPI(ledtype=LEDTYPE.APA102, num=4, **self.SPD)
        expected = [0, 0, 0, 0, 0, 8, 0, 0, 46, 0, 1, 125]
        self.do_test(driver, expected)

    def test_lpd8806(self):
        driver = SPI(ledtype=LEDTYPE.LPD8806, num=4, **self.SPD)
        expected = [
            128, 128, 128, 128, 128, 132, 128, 128, 151, 128, 128, 190, 0]
        self.do_test(driver, expected)

    def test_ws2801(self):
        driver = SPI(ledtype=LEDTYPE.WS2801, num=4, **self.SPD)
        expected = [0, 0, 0, 0, 0, 8, 0, 0, 45, 0, 0, 125]
        self.do_test(driver, expected)
