import unittest

from bibliopixel.util import AttributeDict


class AttributeDictTest(unittest.TestCase):
    def test_simple(self):
        d = AttributeDict()
        with self.assertRaises(AttributeError):
            d.foo

    def test_single(self):
        d = AttributeDict()
        d.foo = 1
        self.assertEqual(d.foo, 1)

        d2 = AttributeDict(foo=1)
        self.assertEqual(d2.foo, 1)
        self.assertEqual(d, d2)

    def test_sub(self):
        d = AttributeDict()
        d.foo = {}
        self.assertTrue(not d.foo)

        d2 = AttributeDict(foo={})
        self.assertTrue(not d2.foo)
        self.assertEqual(d, d2)

        d.foo.bar = 12
        d.foo.baz = 'a'
        d.foo.bang = dict(a=1, b=2)
        self.assertIsInstance(d.foo.bang, AttributeDict)
        self.assertNotEqual(d, d2)
