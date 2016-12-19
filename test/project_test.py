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
        "max_steps": 5
    }
}
"""


class ProjectTest(unittest.TestCase):
    def test_simple(self):
        project.Project(**json.loads(PROJECT)).run()
