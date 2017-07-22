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


PROJECT_NUMPY = """
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
        "use_numpy": true
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
        "typename": "bibliopixel.animation.tests.StripChannelTest",
        "name": "test name",
        "data": {"title": "test title"}
    },

    "run": {
        "max_steps": 2
    }
}
"""

PROJECT_SEQUENCE = """
{
    "driver": "dummy",
    "layout": "matrix",

    "animation": {
        "typename": "sequence",

        "animations": [
            "matrix_test",
            {
                "typename": "matrix_test",
                "name": "mt",
                "data": {"title": "test title"}
            },
            {
                "animation": {
                    "typename": "matrix_test",
                    "name": "mt2",
                    "data": {"title": "test title"}
                }
            }
        ]
    }
}
"""

PROJECT_FAILURE1 = """
{
    "driver": {
        "typename": "test.failure.Failure",
        "num": 12
    },

    "layout": {
        "typename": "bibliopixel.layout.strip.Strip"
    },

    "animation": {
        "typename": "bibliopixel.animation.tests.StripChannelTest"
    }
}
"""


PROJECT_FAILURE2 = """
{
    "driver": {
        "typename": "test.failure2.NON_EXISTENT",
        "num": 12
    },

    "layout": {
        "typename": "bibliopixel.layout.strip.Strip"
    },

    "animation": {
        "typename": "bibliopixel.animation.tests.StripChannelTest"
    }
}
"""


PROJECT_FAILURE3 = """
{
    "driver": {
        "typename": "test.NON_EXISTENT.Failure",
        "num": 12
    },

    "layout": {
        "typename": "bibliopixel.layout.strip.Strip"
    },

    "animation": {
        "typename": "bibliopixel.animation.tests.StripChannelTest"
    }
}
"""


def make(name, is_json=True, run_start=not SKIP_LONG_TESTS):
    animation = run.make_animation(name, is_json, None)
    if run_start:
        animation.start()
    return animation


class ProjectTest(unittest.TestCase):
    def test_bad_json(self):
        with self.assertRaises(ValueError):
            make('{]')

    def test_simple(self):
        make(PROJECT)

    def test_types(self):
        animation = make(PROJECT_TYPES)
        kwds = animation.layout.drivers[0]._kwds
        self.assertEquals(kwds['c_order'], (1, 2, 0))
        self.assertEquals(kwds['color'], (0, 255, 0))
        self.assertEquals(kwds['duration'], 3720)
        self.assertEquals(kwds['gamma'], gamma.APA102)
        self.assertEquals(kwds['time'], 35000)
        self.assertEquals(kwds['ledtype'], LEDTYPE.GENERIC)

    def test_file(self):
        make('test/project.json', False)

    def test_multi(self):
        animation = make(PROJECT_MULTI)
        k = [d._kwds for d in animation.layout.drivers]
        self.assertEquals(k[0]['width'], 128)
        self.assertEquals(k[1]['width'], 128)
        self.assertEquals(k[2]['width'], 128)
        self.assertEquals(k[0]['device_id'], 10)
        self.assertEquals(k[1]['device_id'], 11)
        self.assertEquals(k[2]['device_id'], 12)

    def test_shared(self):
        make(PROJECT_SHARED)

    def test_sequence(self):
        animation = make(PROJECT_SEQUENCE, run_start=False)
        self.assertEquals(len(animation.animations), 3)
        animation = animation.animations[1]
        self.assertEquals(animation.name, 'mt')

    def test_numpy(self):
        make(PROJECT_NUMPY)

    def test_sim(self):
        animation = make(PROJECT_SIM, run_start=False)
        self.assertEquals(animation.name, 'test name')
        self.assertEquals(animation.data, {'title': 'test title'})

    def test_failure1(self):
        with self.assertRaises(ImportError) as e:
            make(PROJECT_FAILURE1)
        self.assertEquals(e.exception.name, 'nonexistent_module')

    def test_failure2(self):
        with self.assertRaises(ImportError) as e:
            make(PROJECT_FAILURE2)
        self.assertEquals(e.exception.name, 'test.failure2.NON_EXISTENT')

    def test_failure3(self):
        with self.assertRaises(ImportError) as e:
            make(PROJECT_FAILURE3)
        self.assertEquals(e.exception.name, 'test.NON_EXISTENT')
