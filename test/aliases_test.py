import unittest
from bibliopixel.project.aliases import resolve_aliases


class AliasTest(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(resolve_aliases({}), {})

    def test_simple(self):
        self.assertEqual(resolve_aliases({'led': {}}), {'led': {}})
        d = {'led': {'typename': 'bibliopixel.layout.circle.Circle'}}
        self.assertEqual(resolve_aliases(d), d)

    def test_resolve(self):
        d = {'led': {'typename': 'bibliopixel.layout.circle.Circle'}}
        self.assertEqual(resolve_aliases({'led': 'circle'}), d)
        self.assertEqual(resolve_aliases({'led': {'typename': 'circle'}}), d)
