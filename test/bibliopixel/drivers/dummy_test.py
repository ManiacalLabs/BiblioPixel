import argparse, time, unittest

from bibliopixel.layout.strip import Strip
from bibliopixel.drivers.dummy import Dummy
from bibliopixel.project import clock


def clock_only_project():
    return argparse.Namespace(clock=clock.Clock())


class DummyTest(unittest.TestCase):
    def test_dummy(self):
        for driver in Dummy(32), Dummy(32, 0.01):
            driver.set_project(clock_only_project())
            layout = Strip([driver])
            layout.push_to_driver()
