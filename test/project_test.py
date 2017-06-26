import json, unittest

from bibliopixel.main import run
from bibliopixel import gamma
from bibliopixel.drivers.serial import codes
from . mark_tests import SKIP_LONG_TESTS


PROJECT = """
{
    "driver": {
        "typename": "dummy",
        "num": 12
    },

    "layout": "strip",
    "animation": "strip_test",
    "run": {
        "max_steps": 2
    }
}
"""

PROJECT_TYPES = """
{
    "driver": {
        "typename": "dummy",
        "num": 12,

        "c_order": "GBR",
        "color": "green",
        "duration": "1 hour, 2 minutes",
        "gamma": "APA102",
        "ledtype": "WS2812",
        "time": "35ks",
        "type": "GENERIC"
    },

    "layout": "strip",
    "animation": "strip_test",
    "run": {
        "max_steps": 2
    }
}
"""

PROJECT_MULTI = """
{
    "driver": {
        "typename": "dummy",
        "multi": true,
        "width": 128,
        "height": 32,
        "num": 4096,
        "device_ids": [10, 11, 12]
    },

    "layout": {
        "typename": "matrix",
        "width": 128
    },

    "animation": "matrix_test",

    "run": {
        "max_steps": 2
    }
}
"""


PROJECT_SHARED = """
{
    "driver": {
        "typename": "dummy",
        "num": 12
    },

    "layout": "strip",
    "animation": "strip_test",
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
        "typename": "bibliopixel.drivers.SimPixel.SimPixel",
        "num": 12
    },

    "layout": {
        "typename": "bibliopixel.layout.strip.Strip"
    },

    "animation": {
        "typename": "bibliopixel.animation.tests.StripChannelTest"
    },

    "run": {
        "max_steps": 2
    }
}
"""


def start(name, is_json=True):
    animation = run.project_to_animation(name, is_json, None)
    if not SKIP_LONG_TESTS:
        animation.start()
    return animation


class ProjectTest(unittest.TestCase):
    def test_simple(self):
        start(PROJECT)

    def test_types(self):
        animation = start(PROJECT_TYPES)
        kwds = animation.layout.drivers[0]._kwds
        self.assertEquals(kwds['c_order'], (1, 2, 0))
        self.assertEquals(kwds['color'], (0, 255, 0))
        self.assertEquals(kwds['duration'], 3720)
        self.assertEquals(kwds['gamma'], gamma.APA102)
        self.assertEquals(kwds['ledtype'], codes.LEDTYPE.WS2812)
        self.assertEquals(kwds['time'], 35000)
        self.assertEquals(kwds['type'], codes.LEDTYPE.GENERIC)

    def test_file(self):
        start('test/project.json', False)

    def test_multi(self):
        start(PROJECT_MULTI)

    def test_shared(self):
        start(PROJECT_SHARED)

    def test_sim(self):
        start(PROJECT_SIM)
