import json, unittest

from bibliopixel.project import project
from . long_test import long_test


PROJECT = """
{
    "driver": {
        "typename": "bibliopixel.drivers.dummy_driver.DriverDummy",
        "num": 12
    },

    "led": {
        "typename": "bibliopixel.led.strip.LEDStrip"
    },

    "animation": {
        "typename": "bibliopixel.animation.tests.StripChannelTest"
    },

    "run": {
        "max_steps": 2
    }
}
"""

PROJECT_MULTI = """
{
    "driver": {
        "typename": "bibliopixel.drivers.dummy_driver.DriverDummy",
        "multi": true,
        "width": 128,
        "height": 32,
        "num": 4096,
        "device_ids": [10, 11, 12]
    },

    "led": {
        "typename": "bibliopixel.led.matrix.LEDMatrix",
        "width": 128
    },

    "animation": {
        "typename": "bibliopixel.animation.tests.MatrixChannelTest"
    },

    "run": {
        "max_steps": 2
    }
}
"""


PROJECT_SHARED = """
{
    "driver": {
        "typename": "bibliopixel.drivers.dummy_driver.DriverDummy",
        "num": 12
    },

    "led": {
        "typename": "bibliopixel.led.strip.LEDStrip"
    },

    "animation": {
        "typename": "bibliopixel.animation.tests.StripChannelTest"
    },

    "run": {
        "max_steps": 2
    },

    "maker": {
        "shared_memory": true
    }
}
"""


PROJECT_SIM = """
{
    "driver": {
        "typename": "bibliopixel.drivers.SimPixel.DriverSimPixel",
        "num": 12
    },

    "led": {
        "typename": "bibliopixel.led.strip.LEDStrip"
    },

    "animation": {
        "typename": "bibliopixel.animation.tests.StripChannelTest"
    },

    "run": {
        "max_steps": 2
    }
}
"""


class ProjectTest(unittest.TestCase):
    @long_test
    def test_simple(self):
        project.run(PROJECT)

    @long_test
    def test_file(self):
        project.run('test/project.json')

    @long_test
    def test_multi(self):
        project.run(PROJECT_MULTI)

    @long_test
    def test_shared(self):
        project.run(PROJECT_SHARED)

    @long_test
    def test_sim(self):
        project.run(PROJECT_SIM)
