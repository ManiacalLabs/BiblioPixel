import unittest
from bibliopixel.project.aliases import resolve_aliases


class AliasTest(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(resolve_aliases({}), {})

    def test_simple(self):
        self.assertEqual(resolve_aliases({'led': {}}), {'led': {}})
        d = {'led': {'typename': 'bibliopixel.led.circle.LEDCircle'}}
        self.assertEqual(resolve_aliases(d), d)

    def test_resolve(self):
        d = {'led': {'typename': 'bibliopixel.led.circle.LEDCircle'}}
        self.assertEqual(resolve_aliases({'led': 'circle'}), d)
        self.assertEqual(resolve_aliases({'led': {'typename': 'circle'}}), d)

    def test_sequence(self):
        d = {
            'animation': {
                'typename': 'sequence',
                'animations': [
                    'matrix_test',
                    'strip_test',
                ],
            }
        }
        result = {
            'animation': {
                'typename': 'bibliopixel.animation.Sequence',
                'animations': [
                    {'typename':
                     'bibliopixel.animation.tests.MatrixChannelTest'},
                    {'typename':
                     'bibliopixel.animation.tests.StripChannelTest'}]}}
        self.assertEqual(resolve_aliases(d), result)
