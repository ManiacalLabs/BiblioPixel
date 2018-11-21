import unittest
from bibliopixel.colors import tables


class TablesTest(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(tables.get_color('RED'), (255, 0, 0))
        self.assertEqual(tables.get_name((255, 0, 0)), 'red')
        self.assertIs(tables.get_color('rod'), None)

    def test_new_colors(self):
        self.assertIs(tables.get_color('frog'), None)

        frog = 1, 255, 2
        tables.set_user_colors({'Frog': frog})
        try:
            self.assertEqual(tables.get_color('RED'), (255, 0, 0))
            self.assertEqual(tables.get_name((255, 0, 0)), 'red')
            self.assertEqual(tables.get_color('frog'), frog)
            self.assertEqual(tables.get_name(frog), 'Frog')
        finally:
            tables.set_user_colors({})

        self.assertIs(tables.get_color('frog'), None)

    def test_override_colors(self):
        self.assertEqual(tables.get_color('RED'), (255, 0, 0))
        self.assertEqual(tables.get_name((255, 0, 0)), 'red')

        wrong_red = 6, 6, 6
        tables.set_user_colors({'red': wrong_red})
        try:
            self.assertEqual(tables.get_color('RED'), wrong_red)
            self.assertEqual(tables.get_name(wrong_red), 'red')
            # Ooops! but what else to do?
            self.assertEqual(tables.get_name((255, 0, 0)), 'red')
        finally:
            tables.set_user_colors({})

        self.assertEqual(tables.get_color('RED'), (255, 0, 0))
        self.assertEqual(tables.get_name((255, 0, 0)), 'red')
