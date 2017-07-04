import json, unittest

from bibliopixel.main import run
from bibliopixel import gamma
from bibliopixel.drivers.ledtype import LEDTYPE
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
        "time": "35ks",
        "ledtype": "GENERIC"
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
        "width": 128,
        "height": 32,
        "num": 4096
    },

    "drivers": [
        {"device_id": 10},
        {"device_id": 11},
        {"device_id": 12}
    ],

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
    animation = run.make_animation(name, is_json, None)
    if not SKIP_LONG_TESTS:
        animation.start()
    return animation


class ProjectTest(unittest.TestCase):
    def test_bad_json(self):
        with self.assertRaises(ValueError):
            start('{]')

    def test_simple(self):
        start(PROJECT)

    def test_types(self):
        animation = start(PROJECT_TYPES)
        kwds = animation.layout.drivers[0]._kwds
        self.assertEquals(kwds['c_order'], (1, 2, 0))
        self.assertEquals(kwds['color'], (0, 255, 0))
        self.assertEquals(kwds['duration'], 3720)
        self.assertEquals(kwds['gamma'], gamma.APA102)
        self.assertEquals(kwds['time'], 35000)
        self.assertEquals(kwds['ledtype'], LEDTYPE.GENERIC)

    def test_file(self):
        start('test/project.json', False)

    def test_multi(self):
        animation = start(PROJECT_MULTI)
        k = [d._kwds for d in animation.layout.drivers]
        self.assertEquals(k[0]['width'], 128)
        self.assertEquals(k[1]['width'], 128)
        self.assertEquals(k[2]['width'], 128)
        self.assertEquals(k[0]['device_id'], 10)
        self.assertEquals(k[1]['device_id'], 11)
        self.assertEquals(k[2]['device_id'], 12)

    def test_shared(self):
        start(PROJECT_SHARED)

    def test_sim(self):
        start(PROJECT_SIM)
