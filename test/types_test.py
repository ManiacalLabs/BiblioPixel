import unittest

from bibliopixel.project.types import make, defaults
from bibliopixel import colors, gamma
from bibliopixel.drivers import channel_order


class TypesBaseTest(unittest.TestCase):
    def make(self, name, c, result=None):
        component = make.component({name: c}, field_types=defaults.FIELD_TYPES)
        if result is not None:
            self.assertEquals(component, {name: result})
        return component


class ColorTypesTest(TypesBaseTest):
    def test_unchanged(self):
        for p in {}, {'a': {}}, {'a': {'b': 'c'}}:
            self.assertEqual(make.project(p, {}), p)
            self.assertEqual(make.project(p, defaults.FIELD_TYPES), p)

    def test_color_names(self):
        # Test every color.
        for name in dir(colors):
            if name.istitle():
                c = getattr(colors, name)
                for n in name, name.lower(), name.upper():
                    self.make('color', n, c)

    def test_color_numbers(self):
        for i in range(256):
            self.make('color', i, (i, i, i))

        for c in [0, 0, 0], [127, 128, 255], [4, 200, 77]:
            self.make('color', c, tuple(c))

        for c in (0, 0, 0), (127, 128, 255), (4, 200, 77):
            self.make('color', c, c)

    def test_errors(self):
        with self.assertRaises(ValueError):
            self.make('color', -1)

        with self.assertRaises(ValueError):
            self.make('color', 256)

        with self.assertRaises(ValueError):
            self.make('color', '')

        with self.assertRaises(ValueError):
            self.make('color', '255')

        with self.assertRaises(ValueError):
            self.make('color', '[0, 0, 0]')

        with self.assertRaises(ValueError):
            self.make('color', '(0, 0, 0)')

        with self.assertRaises(ValueError):
            self.make('color', 'dog')

        with self.assertRaises(ValueError):
            self.make('color', ())

        with self.assertRaises(ValueError):
            self.make('color', (1,))

        with self.assertRaises(ValueError):
            self.make('color', (1, 2))

        self.make('color', (1, 2, 3))

        with self.assertRaises(ValueError):
            self.make('color', (1, 2, 3, 4))


class DurationTypesTest(TypesBaseTest):
    def test_some(self):
        self.make('duration', '1', 1)
        self.make('duration', '1s', 1)
        self.make('duration', '2.5s', 2.5)
        self.make('duration', '10 mins, 2.5s', 602.5)


class LEDTYPETypesTest(TypesBaseTest):
    def test_some(self):
        self.make('ledtype', 'LPD8806')
        self.make('ledtype', 'GENERIC')

        with self.assertRaises(ValueError):
            self.make('ledtype', 2)

        with self.assertRaises(KeyError):
            self.make('ledtype', 'NONE')


class GammaTypesTest(TypesBaseTest):
    def test_some(self):
        self.make('gamma', 'LPD8806', gamma.LPD8806)
        self.make('gamma', 'DEFAULT', gamma.DEFAULT)

        gam = self.make('gamma', {'gamma': 2.5, 'offset': 0.5})
        self.assertEquals(gam['gamma'].table, gamma.APA102.table)

        gam = self.make('gamma', [2.5, 0.5, 128])
        self.assertEquals(gam['gamma'].table, gamma.LPD8806.table)

        with self.assertRaises(TypeError):
            self.make('gamma', [0, 1, 2, 3])

        with self.assertRaises(ValueError):
            self.make('gamma', None)


class ChannelOrderTypesTest(TypesBaseTest):
    def test_some(self):
        def test(i, *cases):
            expected = channel_order.ChannelOrder.ORDERS[i]
            for case in cases:
                actual = self.make('c_order', case)['c_order']
                self.assertIs(expected, actual)

        test(0, 'rgb', (0, 1, 2), [0, 1, 2], '012')
        test(5, 'bgr', (2, 1, 0), [2, 1, 0], 'b1R')

        with self.assertRaises(IndexError):
            self.make('c_order', -1)

        with self.assertRaises(IndexError):
            self.make('c_order', 6)

        with self.assertRaises(KeyError):
            self.make('c_order', 'NONE')

        with self.assertRaises(ValueError):
            self.make('c_order', 'RGG')

        with self.assertRaises(ValueError):
            self.make('c_order', None)
