import unittest

from bibliopixel.layout.strip import Strip
from bibliopixel.drivers.dummy_driver import Dummy


class DummyTest(unittest.TestCase):
    def test_dummy(self):
        for driver in Dummy(32), Dummy(32, 0.01):
            layout = Strip([driver])
            layout.push_to_driver()
