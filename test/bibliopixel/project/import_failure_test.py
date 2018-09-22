import unittest
from unittest import mock

from . make import make


PROJECT_FAILURE1 = """
{
    "driver": {
        "typename": "test.bibliopixel.failure.Failure",
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
        "typename": "test.bibliopixel.failure2.NON_EXISTENT",
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

BAD_JSON_ERROR = """
while parsing a flow node
expected the node content, but found ']'
  in "<unicode string>", line 1, column 2:
    {]
     ^
"""


class ImportFailureTest(unittest.TestCase):
    @mock.patch('bibliopixel.util.data_file.ALWAYS_LOAD_YAML', False)
    def test_bad_import_json(self):
        with self.assertRaises(Exception):
            make('{]')

    @mock.patch('bibliopixel.util.data_file.ALWAYS_LOAD_YAML', True)
    def test_bad_import_yaml(self):
        with self.assertRaises(Exception) as e:
            make('{]')

        self.assertEqual(str(e.exception).strip(), BAD_JSON_ERROR.strip())

    def test_failure1(self):
        with self.assertRaises(ImportError) as e:
            make(PROJECT_FAILURE1)
        self.assertEqual(e.exception.name, 'test.bibliopixel.failure.Failure')

    def test_failure2(self):
        with self.assertRaises(ImportError) as e:
            make(PROJECT_FAILURE2)
        self.assertEqual(e.exception.name,
                         'test.bibliopixel.failure2.NON_EXISTENT')

    def test_failure3(self):
        with self.assertRaises(ImportError) as e:
            make(PROJECT_FAILURE3)
        self.assertEqual(e.exception.name, 'test.NON_EXISTENT.Failure')
