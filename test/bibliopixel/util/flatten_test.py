import unittest

from bibliopixel.util.flatten import canonical, flatten, unflatten


class FlattenTest(unittest.TestCase):
    def assert_flatten(self, before, after=None):
        self.assertEqual(flatten(before), after or before)
        self.assertEqual(flatten(flatten(before)), after or before)
        after and self.assertEqual(canonical(before), canonical(after))

    def assert_unflatten(self, before, after=None):
        self.assertEqual(before, unflatten(after or before))
        self.assertEqual(before, unflatten(unflatten(after or before)))
        after and self.assertEqual(canonical(before), canonical(after))

    def test_trivial(self):
        self.assert_flatten({})

    def test_simple(self):
        before = {'a': 1, 'c': {'d': True}}
        after = {'a': 1, 'c.d': True}
        self.assert_flatten(before, after)
        self.assert_unflatten(before, after)

    def test_three_levels(self):
        before = {'foo': {'bar': {'a': 1, 'b': True, 'c': 'X'}}}
        after = {'foo.bar.a': 1, 'foo.bar.b': True, 'foo.bar.c': 'X'}
        self.assert_flatten(before, after)
        self.assert_unflatten(before, after)

    def test_mix(self):
        before = {'foo': {'bar': {'a': 1}, 'bar.c': 'X'}, 'foo.bar.b': True}
        after = {'foo.bar.a': 1, 'foo.bar.b': True, 'foo.bar.c': 'X'}
        canon = {'foo': {'bar': {'a': 1, 'b': True, 'c': 'X'}}}
        self.assert_flatten(before, after)
        self.assert_unflatten(canon, after)
        self.assertEqual(canonical(before), canon)

    def test_error(self):
        with self.assertRaises(ValueError):
            flatten({'foo': {'bar': {'b': True}}, 'foo.bar.b': True})

        with self.assertRaises(ValueError):
            flatten({'foo.bar': {'b': True}, 'foo': {'bar.b': True}})
