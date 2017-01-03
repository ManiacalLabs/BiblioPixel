import json, unittest

from bibliopixel.util import project

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
        "typename": "bibliopixel.led.matrix.LEDMatrix"
    },

    "animation": {
        "typename": "bibliopixel.animation.tests.MatrixChannelTest"
    },

    "run": {
        "max_steps": 2
    }
}
"""


class ProjectTest(unittest.TestCase):
    def test_simple(self):
        project.run(PROJECT)

    def test_file(self):
        project.run('test/project.json')

    def test_multi(self):
        project.run(PROJECT_MULTI)
