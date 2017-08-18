import os, unittest
from . import_all import import_all

BLACKLIST = ['bibliopixel.drivers.PiWS281X']
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class ImportAllTest(unittest.TestCase):
    def test_all(self):
        _, failures = import_all(PROJECT_ROOT, 'bibliopixel', BLACKLIST)
        self.assertEqual(failures, [])
