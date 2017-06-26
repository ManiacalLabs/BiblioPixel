import unittest
from bibliopixel.project.types import make, color
from bibliopixel import colors


class TypesTest(unittest.TestCase):
    def test_unchanged(self):
        for p in {}, {'a': {}}, {'a': {'b': 'c'}}:
            self.assertEqual(make.project(p, {}), p)
            self.assertEqual(make.project(p, {'color': color}), p)

    def make_color(self, c, result=None):
        component = make.component({'color': c}, {'color': color})
        if result is not None:
            self.assertEquals(component, {'color': result})

    def test_color_names(self):
        # Test every color.
        for name in dir(colors):
            if name.istitle():
                c = getattr(colors, name)
                for n in name, name.lower(), name.upper():
                    self.make_color(n, c)

    def test_color_numbers(self):
        for i in range(256):
            self.make_color(i, (i, i, i))

        for c in [0, 0, 0], [127, 128, 255], [4, 200, 77]:
            self.make_color(c, tuple(c))

        for c in (0, 0, 0), (127, 128, 255), (4, 200, 77):
            self.make_color(c, c)

    def test_errors(self):
        with self.assertRaises(ValueError):
            self.make_color(-1)

        with self.assertRaises(ValueError):
            self.make_color(256)

        with self.assertRaises(ValueError):
            self.make_color('')

        with self.assertRaises(ValueError):
            self.make_color('255')

        with self.assertRaises(ValueError):
            self.make_color('[0, 0, 0]')

        with self.assertRaises(ValueError):
            self.make_color('(0, 0, 0)')

        with self.assertRaises(ValueError):
            self.make_color('dog')

        with self.assertRaises(ValueError):
            self.make_color(())

        with self.assertRaises(ValueError):
            self.make_color((1,))

        with self.assertRaises(ValueError):
            self.make_color((1, 2))

        self.make_color((1, 2, 3))

        with self.assertRaises(ValueError):
            self.make_color((1, 2, 3, 4))
