import unittest
from bibliopixel.util import int_names


class NamesTest(unittest.TestCase):
    def test_to_index(self):
        self.assertEqual(int_names.to_index('H'), 1)
        self.assertEqual(int_names.to_index('hydrogen'), 1)
        self.assertEqual(int_names.to_index('wed'), 3)
        self.assertEqual(int_names.to_index('wednesday'), 3)
        self.assertEqual(int_names.to_index('Pluto'), 9)
        with self.assertRaises(KeyError):
            int_names.to_index('Ploto')
        with self.assertRaises(KeyError):
            int_names.to_index('12.5')
        with self.assertRaises(KeyError):
            int_names.to_index(12.5)

    def test_to_names(self):
        expected = ['Mon', 'Monday', 'Jan', 'January', 'red', 'Mercury', 'H',
                    'hydrogen']
        self.assertEqual(int_names.to_names(1), expected)
        self.assertEqual(int_names.to_names(98), ['Cf', 'californium'])
        with self.assertRaises(KeyError):
            int_names.to_names(126)
