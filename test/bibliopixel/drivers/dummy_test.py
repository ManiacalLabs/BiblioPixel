import argparse, time, unittest

from bibliopixel.layout.strip import Strip
from bibliopixel.drivers.dummy_driver import Dummy


def clock_only_project():
    return argparse.Namespace(time=time.time, sleep=time.sleep)


class DummyTest(unittest.TestCase):
    def test_dummy(self):
        for driver in Dummy(32), Dummy(32, 0.01):
            driver.set_project(clock_only_project())
            layout = Strip([driver])
            layout.push_to_driver()
