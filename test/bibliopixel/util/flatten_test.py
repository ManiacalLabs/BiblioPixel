import unittest

from bibliopixel.util.flatten import flatten


class FlattenTest(unittest.TestCase):
    def assert_flatten(self, before, after=None):
        self.assertEqual(flatten(before), after or before)
        self.assertEqual(flatten(flatten(before)), after or before)

    def test_trivial(self):
        self.assert_flatten({})

    def test_simple(self):
        self.assert_flatten({'a': 1, 'c.d': True})

    def test_three_levels(self):
        before = {'foo': {'bar': {'a': 1, 'b': True, 'c': 'X'}}}
        after = {'foo.bar.a': 1, 'foo.bar.b': True, 'foo.bar.c': 'X'}
        self.assert_flatten(before, after)

    def test_mix(self):
        before = {'foo': {'bar': {'a': 1}, 'bar.c': 'X'}, 'foo.bar.b': True}
        after = {'foo.bar.a': 1, 'foo.bar.b': True, 'foo.bar.c': 'X'}
        self.assert_flatten(before, after)

    def test_error(self):
        with self.assertRaises(ValueError):
            flatten({'foo': {'bar': {'b': True}}, 'foo.bar.b': True})

        with self.assertRaises(ValueError):
            flatten({'foo.bar': {'b': True}, 'foo': {'bar.b': True}})
