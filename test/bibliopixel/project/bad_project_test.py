import json, unittest
from bibliopixel.project import project

from . make import make


PYTHON_FILE = 'driver = {"a": "b"}'
MISSING_LAYOUT = '{"animation": "off", "driver": "dummy"}'


BAD_SECTION = """
{
    "bad_section": {"foo": true},
    "driver": "dummy",
    "layout": "matrix",
    "animation": "off"
}
"""

BAD_SECTION2 = """
{
    "verbose": true,
    "driver": "dummy",
    "layout": "matrix",
    "animation": "off"
}
"""

MISSING_DATATYPE = """
{
    "driver": {
         "width": 16,
         "height": 16
    },
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
            ('There was a error in the data file',
             'Expecting value: line 1 column 1 (char 0)'))

    def test_cant_open(self):
        with self.assertRaises(FileNotFoundError) as e:
            make('this-file-does-not-exist.json')

        self.assertEquals(e.exception.args, (2, 'No such file or directory'))

    def test_bad_section(self):
        with self.assertRaises(ValueError) as e:
            make(BAD_SECTION)

        self.assertEquals(
            e.exception.args,
            ('There is no Project section named "bad_section"',))

    def test_bad_section2(self):
        # See https://github.com/ManiacalLabs/BiblioPixel/issues/787
        with self.assertRaises(ValueError) as e:
            make(BAD_SECTION2)

        self.assertEquals(
            e.exception.args,
            ('There is no Project section named "verbose"',))

    def test_missing_datatype(self):
        with self.assertRaises(ValueError) as e:
            make(MISSING_DATATYPE)
        self.assertEquals(
            e.exception.args,
            ('Unable to create drivers',
             'No "datatype" field in section "drivers"'))

    def test_bad_driver_attribute(self):
        with self.assertRaises(ValueError) as e:
            make(BAD_DRIVER_ATTRIBUTE)
        self.assertEquals(
            e.exception.args,
            ('Unable to create drivers',
             'Unknown attribute for driver SimPixel: "bad_attribute"',))

    def test_bad_layout_attribute(self):
        with self.assertRaises(ValueError) as e:
            make(BAD_LAYOUT_ATTRIBUTE)
        self.assertEquals(
            e.exception.args,
            ('Unable to create layout',
             'Unknown attribute for layout Matrix: "bad_attribute"'))

    def test_bad_animation_attribute(self):
        animation = make(BAD_ANIMATION_ATTRIBUTE, run_start=False)
        self.assertEquals(
            animation.exception.args,
            ('Unknown attribute for animation Off: "bad_attribute"',))

    def test_bad_run_attribute(self):
        animation = make(BAD_RUN_ATTRIBUTE, run_start=False)
        self.assertEquals(
            animation.exception.args,
            ('Unknown attribute for run: "bad_attribute"',))

    def test_missing_layout(self):
        with self.assertRaises(ValueError) as e:
            make(MISSING_LAYOUT)
        self.assertEquals(
            e.exception.args,
            ('Missing "layout" section',))

    def test_missing_everything(self):
        with self.assertRaises(ValueError) as e:
            make('{}')
        self.assertEquals(
            e.exception.args,
            ('Missing "layout" section',))
