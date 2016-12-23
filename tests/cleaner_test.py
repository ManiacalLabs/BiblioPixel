import unittest
from bibliopixel.util.cleaner import cleaner


class CleanerTest(unittest.TestCase):
    def test_simple(self):
        class Cleanable(object):
            def cleanup(self):
                self.cleaned = True
        c = Cleanable()
        with cleaner(c):
            with self.assertRaises(AttributeError):
                c.cleaned
        self.assertTrue(c.cleaned)
