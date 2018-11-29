import unittest
from unittest import mock

from . make import make
from bibliopixel.animation import animation
from bibliopixel.colors import gamma, tables
from bibliopixel.drivers.ledtype import LEDTYPE

BAD_JSON_ERROR = """
while parsing a flow node
expected the node content, but found ']'
  in "<unicode string>", line 1, column 2:
    {]
     ^
"""


class ProjectTest(unittest.TestCase):
    @mock.patch('bibliopixel.util.data_file.ALWAYS_LOAD_YAML', False)
    def test_bad_project_json(self):
        with self.assertRaises(Exception):
            make('{]')

    @mock.patch('bibliopixel.util.data_file.ALWAYS_LOAD_YAML', True)
    def test_bad_project_yaml(self):
        with self.assertRaises(Exception) as e:
            make('{]')

        self.assertEqual(str(e.exception).strip(), BAD_JSON_ERROR.strip())

    def test_simple(self):
        make(PROJECT)

    def test_types(self):
        animation = make(PROJECT_TYPES)
        kwds = animation.layout.drivers[0]._kwds
        self.assertEqual(kwds['c_order'], (1, 2, 0))
        self.assertEqual(kwds['color'], (0, 255, 0))
        self.assertEqual(kwds['duration'], 3720)
        self.assertEqual(kwds['gamma'].table, gamma.APA102.table)
        self.assertEqual(kwds['time'], 35000)
        self.assertEqual(kwds['ledtype'], LEDTYPE.GENERIC)

    def test_file(self):
        make('test/bibliopixel/project/project.json', False)

    def test_yaml_file(self):
        make('test/bibliopixel/project/project.yml', False)

    def test_super(self):
        animation = make('test/bibliopixel/project/super_project.json', False)
        self.assertEqual(animation.__class__.__name__, 'StripChannelTest')
        self.assertEqual(animation.layout.pixelWidth, 2)

    def test_multi(self):
        animation = make(PROJECT_MULTI)
        k = [d._kwds for d in animation.layout.drivers]
        self.assertEqual(k[0]['device_id'], 10)
        self.assertEqual(k[1]['device_id'], 11)
        self.assertEqual(k[2]['device_id'], 12)

    def test_shared(self):
        make(PROJECT_SHARED)

    def test_sequence(self):
        animation = make(PROJECT_SEQUENCE, run_start=False)
        self.assertEqual(len(animation.animations), 3)
        self.assertIsNotNone(animation.animations[0])
        animation = animation.animations[1]
        self.assertEqual(animation.name, 'mt')
        self.assertEqual(animation.layout.rotation, 90)

    def test_sub_animation_names(self):
        animation = make(PROJECT_SUB_ANIMATIONS, run_start=False)

        self.assertEqual(animation.name, 'Sequence')
        a, b, c, d = animation.animations
        self.assertEqual(a.name, 'StripChannelTest_0')
        self.assertEqual(d.name, 'StripChannelTest_3')
        animation.pre_run()
        self.assertEqual(animation.animations.StripChannelTest_2, c)
        self.assertEqual(animation.animations['StripChannelTest_1'], b)

    def test_numpy(self):
        make(PROJECT_NUMPY)

    def test_pixelwidth(self):
        make(PROJECT_PIXELWIDTH)

    def test_aliases(self):
        make(PROJECT_ALIASES)

    def test_simpixel(self):
        animation = make(PROJECT_SIM, run_start=False)
        self.assertEqual(animation.name, 'test name')
        self.assertEqual(animation.data, {'title': 'test title'})

    def test_project_from_animation_class(self):
        animation = make(PROJECT_ANIMATION)
        self.assertEqual(animation.layout.rotation, 90)

    def test_nested_animation(self):
        make(PROJECT_NESTED_ANIMATION, run_start=False)

    def test_nested_sequence(self):
        make(PROJECT_NESTED_SEQUENCE, run_start=False)

    def test_project_colors(self):
        try:
            make(PROJECT_COLORS, run_start=False)
            self.assertEqual(tables.get_color('bland'), (1, 2, 3))
            self.assertEqual(tables.get_name((3, 2, 1)), 'exciting!!')
            self.assertIs(tables.get_color('exciting'), None)
        finally:
            tables.set_user_colors({})
        self.assertEqual(tables.get_color('bland'), None)

    def test_test_example(self):
        make(PROJECT_TEST_EXAMPLE)


PROJECT = """
{
    "driver": "dummy",
    "shape": 12,
    "layout": "strip",
    "animation": ".tests.StripChannelTest",
    "run": {
        "max_steps": 2
    }
}
"""

PROJECT_TYPES = """
{
    "driver": {
        "typename": "dummy",
        "c_order": "GBR",
        "color": "green",
        "duration": "1 hour, 2 minutes",
        "gamma": "APA102",
        "time": "35ks",
        "ledtype": "GENERIC"
    },

    "shape": 12,
    "layout": "strip",
    "animation": ".tests.StripChannelTest",
    "run": {
        "max_steps": 2
    }
}
"""

PROJECT_MULTI = """
{
    "driver": {
        "typename": "dummy",
        "num": 4096
    },

    "drivers": [
        {"device_id": 10},
        {"device_id": 11},
        {"device_id": 12}
    ],

    "layout": {
        "typename": "matrix",
        "width": 128,
        "height": 32,
        "gen_coord_map": [
            {
              "dx": 32,
              "dy": 32
            },
            {
              "dx": 32,
              "dy": 32
            },
            {
              "dx": 32,
              "dy": 32
            }
        ]
    },

    "animation": ".tests.MatrixChannelTest",

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
    "animation": ".tests.StripChannelTest",
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

    "layout": "bibliopixel.layout.strip.Strip",
    "animation": ".tests.StripChannelTest",
    "run": {
        "max_steps": 2
    },

    "maker": {
        "numpy_dtype": "float"
    }
}
"""


PROJECT_SIM = """
{
    "driver": {
        "typename": ".SimPixel",
        "num": 12,
        "port": 1338
    },

    "layout": {
        "typename": ".strip"
    },

    "animation": {
        "typename": ".tests.StripChannelTest",
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

    "layout": {
        "typename": "matrix",
        "rotation": 92
    },

    "animation": {
        "typename": "sequence",

        "animations": [
            ".tests.MatrixChannelTest",
            {
                "typename": ".tests.MatrixChannelTest",
                "name": "mt",
                "data": {"title": "test title"}
            },
            {
                "animation": {
                    "typename": ".tests.MatrixChannelTest",
                    "name": "mt2",
                    "data": {"title": "test title"}
                }
            }
        ]
    }
}
"""

PROJECT_ALIASES = """
{
    "aliases": {
        "st": "bibliopixel.layout.strip",
        "stc": ".tests.StripChannelTest"
    },

    "driver": {
        "typename": "dummy",
        "num": 12
    },

    "layout": "@st.Strip",
    "animation": "stc",
    "run": {
        "max_steps": 2
    }
}
"""

PROJECT_PIXELWIDTH = """
{
    "driver": {
        "typename": "dummy",
        "num": 12
    },

    "layout": {
        "typename": "strip",
        "pixelWidth": 3
    },

    "animation": ".tests.StripChannelTest",
    "run": {
        "max_steps": 2
    }
}
"""

PROJECT_SUB_ANIMATIONS = """
{
    "driver": {
        "typename": "dummy",
        "num": 12
    },

    "layout": {
        "typename": "strip",
        "pixelWidth": 3
    },

    "animation": {
        "typename": "sequence",
        "animations": [".tests.StripChannelTest",
                       ".tests.StripChannelTest",
                       ".tests.StripChannelTest",
                       ".tests.StripChannelTest"]
    },

    "run": {
        "max_steps": 2
    }
}
"""

PROJECT_ANIMATION = """
{"animation": "test.bibliopixel.project.project_test.AnimationTest"}
"""

PROJECT_NESTED_ANIMATION = """
shape: [32, 32]
animation:
  typename: .wrapper
  animation:
      typename: .wrapper
      animation: $bpa.matrix.bloom
"""

PROJECT_NESTED_SEQUENCE = """
shape: [32, 32]
animation:
  typename: .sequence
  animations:
      - typename: .sequence
        animations:
        - $bpa.matrix.bloom
"""

PROJECT_COLORS = """
shape: 32
animation: .tests.StripChannelTest
colors:
  bland: [1, 2, 3]
  'exciting!!': [3, 2, 1]
"""

PROJECT_TEST_EXAMPLE = """
driver: dummy
shape: [48, 24]
animation: test.bibliopixel.animation.documentation_class.Example26
run:
  max_steps: 4
"""


class AnimationTest(animation.Animation):
    PROJECT = {
        "driver": "dummy",
        "layout": {
            "typename": "matrix",
            "rotation": 92},
        "run": {
            "max_steps": 2},
    }

    def step(self, amt=1):
        pass
