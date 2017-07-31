import unittest
from bibliopixel.project import aliases


class AliasTest(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(aliases.resolve({}), {})

    def test_simple(self):
        self.assertEqual(aliases.resolve({'layout': {}}), {'layout': {}})
        d = {'layout': {'typename': 'bibliopixel.layout.circle.Circle'}}
        self.assertEqual(aliases.resolve(d), d)

    def test_resolve(self):
        d = {'layout': {'typename': 'bibliopixel.layout.circle.Circle'}}
        self.assertEqual(aliases.resolve({'layout': 'circle'}), d)
        self.assertEqual(aliases.resolve({'layout': {'typename': 'circle'}}), d)
