import time, unittest
from bibliopixel.builder.description import Description
from bibliopixel.util import data_file


class DescriptionTest(unittest.TestCase):
    def test_empty(self):
        d = Description()
        self.assertEqual(str(d), '{}')
        self.assertEqual(d.as_dict(), {})

        expected = {
            'aliases': {},
            'animation': {},
            'colors': {},
            'controls': [],
            'driver': {},
            'drivers': [],
            'layout': {},
            'numbers': '',
            'palettes': {},
            'path': '',
            'run': {},
            'shape': ()}
        self.assertEqual(d.desc, expected)
        self.assertEqual(d.animation, {})
        with self.assertRaises(AttributeError):
            d.wombat

        self.assertIn('colors', d)
        self.assertNotIn('colours', d)
        self.assertEqual(sorted(d), sorted(expected))
        directory = [i for i in dir(d) if not i.startswith('_')]
        expected = [
            'aliases',
            'animation',
            'as_dict',
            'clear',
            'colors',
            'controls',
            'desc',
            'driver',
            'drivers',
            'items',
            'layout',
            'numbers',
            'palettes',
            'path',
            'run',
            'shape',
            'update']

        self.assertEqual(directory, expected)

    def test_setting(self):
        d = Description()
        d.animation = '.tests.PixelTester'
        self.assertEqual(d['animation'], {'typename': '.tests.PixelTester'})
        with self.assertRaises(ImportError):
            d.animation = '.nonexistent.Nonexistent'

        d['animation'] = '.tests.StripChannelTest'
        self.assertEqual(d.animation, {'typename': '.tests.StripChannelTest'})

        d.shape = (10, 11)
        self.assertEqual(d.shape, (10, 11))
