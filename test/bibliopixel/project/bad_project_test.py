import json, unittest
from bibliopixel.project import project

from . make import make


PYTHON_FILE = 'driver = {"a": "b"}'
MISSING_LAYOUT = '{"animation": "off", "driver": "dummy"}'
MISSING_ANIMATION = '{"layout": "matrix", "driver": "dummy"}'


# This one works, but prints a warning.
BAD_SECTION = """
{
    "bad_section": {"foo": true},
    "driver": "dummy",
    "layout": "matrix",
    "animation": "off"
}
"""

BAD_DRIVER_ATTRIBUTE = """
{
    "driver": {
         "typename": "simpixel",
         "width": 16,
         "height": 16,
        "bad_attribute": 16
    },
    "layout": "matrix",
    "animation": "off"
}
"""

BAD_LAYOUT_ATTRIBUTE = """
{
    "driver": "dummy",
    "layout": {"typename": "matrix", "bad_attribute": true},
    "animation": "off"
}
"""

BAD_ANIMATION_ATTRIBUTE = """
{
    "driver": "dummy",
    "layout": "matrix",
    "animation": {"typename": "off", "bad_attribute": "hello"}
}

"""
BAD_RUN_ATTRIBUTE = """
{
    "driver": "dummy",
    "layout": "matrix",
    "animation": "off",
    "run": {"bad_attribute": 23.5}
}
"""


class BadProjectTest(unittest.TestCase):
    def test_bad_json(self):
        with self.assertRaises(ValueError) as e:
            make(PYTHON_FILE)

        self.assertEquals(
            e.exception.args[0::2],
            ('There was a JSON error in the file',
             'Expecting value: line 1 column 1 (char 0)'))

    def test_cant_open(self):
        with self.assertRaises(FileNotFoundError) as e:
            make('this-file-does-not-exist.json')

        intro = e.exception.args[:2]
        tail = e.exception.args[-2:]
        self.assertEquals(
            intro, ('There was an error reading the file',
                    'this-file-does-not-exist.json'))
        self.assertEquals(tail, (2, 'No such file or directory'))

    def test_bad_section(self):
        with self.assertRaises(ValueError) as e:
            make(BAD_SECTION)

        self.assertEquals(
            e.exception.args,
            ('Unknown attribute for project: "bad_section"',))

    def test_bad_driver_attribute(self):
        with self.assertRaises(ValueError) as e:
            make(BAD_DRIVER_ATTRIBUTE)
        self.assertEquals(
            e.exception.args,
            ('Unknown attribute for driver SimPixel: "bad_attribute"',))

    def test_bad_layout_attribute(self):
        with self.assertRaises(ValueError) as e:
            make(BAD_LAYOUT_ATTRIBUTE)
        self.assertEquals(
            e.exception.args,
            ('Unable to create layout',
             'Unknown attribute for layout Matrix: "bad_attribute"'))

    def test_bad_animation_attribute(self):
        with self.assertRaises(ValueError) as e:
            make(BAD_ANIMATION_ATTRIBUTE)
        self.assertEquals(
            e.exception.args,
            ('Unable to create animation',
             'Unknown attribute for animation OffAnim: "bad_attribute"'))

    def test_bad_run_attribute(self):
        with self.assertRaises(ValueError) as e:
            make(BAD_RUN_ATTRIBUTE)
        self.assertEquals(
            e.exception.args,
            ('Unknown attribute for run: "bad_attribute"',))

    def test_missing_layout(self):
        with self.assertRaises(ValueError) as e:
            make(MISSING_LAYOUT)
        self.assertEquals(
            e.exception.args,
            ('Missing "layout" section',))

    def test_missing_animation(self):
        with self.assertRaises(ValueError) as e:
            make(MISSING_ANIMATION)
        self.assertEquals(
            e.exception.args,
            ('Missing "animation" section',))

    def test_missing_everything(self):
        with self.assertRaises(ValueError) as e:
            make('{}')
        self.assertEquals(
            e.exception.args,
            ('Missing "animation" section',))
