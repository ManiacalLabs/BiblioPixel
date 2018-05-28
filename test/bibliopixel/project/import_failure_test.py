import unittest

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


class ImportFailureTest(unittest.TestCase):
    def test_bad_json(self):
        with self.assertRaises(ValueError):
            make('{]')

    def test_failure1(self):
        with self.assertRaises(ImportError) as e:
            make(PROJECT_FAILURE1)
        self.assertEquals(e.exception.name, 'test.bibliopixel.failure.Failure')

    def test_failure2(self):
        with self.assertRaises(ImportError) as e:
            make(PROJECT_FAILURE2)
        self.assertEquals(e.exception.name,
                          'test.bibliopixel.failure2.NON_EXISTENT')

    def test_failure3(self):
        with self.assertRaises(ImportError) as e:
            make(PROJECT_FAILURE3)
        self.assertEquals(e.exception.name, 'test.NON_EXISTENT.Failure')
