import unittest
from bibliopixel.project.aliases import resolve_aliases


class AliasTest(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(resolve_aliases({}), {})

    def test_simple(self):
        self.assertEqual(resolve_aliases({'layout': {}}), {'layout': {}})
        d = {'layout': {'typename': 'bibliopixel.layout.circle.Circle'}}
        self.assertEqual(resolve_aliases(d), d)

    def test_resolve(self):
        d = {'layout': {'typename': 'bibliopixel.layout.circle.Circle'}}
        self.assertEqual(resolve_aliases({'layout': 'circle'}), d)
        self.assertEqual(resolve_aliases({'layout': {'typename': 'circle'}}), d)
