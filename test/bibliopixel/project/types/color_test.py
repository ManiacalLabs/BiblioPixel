from . base import TypesBaseTest
from bibliopixel.util import colors
from bibliopixel.project import fields


class ColorTypesTest(TypesBaseTest):
    def test_color_names(self):
        # Test every color.
        for name in dir(colors):
            if name.istitle():
                c = getattr(colors, name)
                for n in name, name.lower(), name.upper():
                    self.make('color', n, c)

    def test_color_numbers(self):
        for i in range(256):
            self.make('color', hex(0x10101 * i), (i, i, i))

        for c in [0, 0, 0], [127, 128, 255], [4, 200, 77]:
            self.make('color', c, tuple(c))

        for c in (0, 0, 0), (127, 128, 255), (4, 200, 77):
            self.make('color', c, c)
            self.make('color', str(c), c)

    def test_errors(self):
        with self.assertRaises(ValueError):
            self.make('color', -1)

        with self.assertRaises(ValueError):
            self.make('color', 256)

        with self.assertRaises(ValueError):
            self.make('color', '')

        with self.assertRaises(ValueError):
            self.make('color', '[0, 0, 0]')

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
