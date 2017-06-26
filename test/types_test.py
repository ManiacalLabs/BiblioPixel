import unittest

from bibliopixel.project.types import make, color, duration, ledtype
from bibliopixel import colors


class TypesBaseTest(unittest.TestCase):
    def make(self, name, c, result=None):
        component = make.component({name: c}, {name: globals()[name]})
        if result is not None:
            self.assertEquals(component, {name: result})


class ColorTypesTest(TypesBaseTest):
    def test_unchanged(self):
        for p in {}, {'a': {}}, {'a': {'b': 'c'}}:
            self.assertEqual(make.project(p, {}), p)
            self.assertEqual(make.project(p, {'color': color}), p)

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
