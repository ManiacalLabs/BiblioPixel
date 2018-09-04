import unittest
from bibliopixel.util import duration


class DurationTest(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(duration.parse('1'), 1)
        self.assertEqual(duration.parse('23.5'), 23.5)

        with self.assertRaises(ValueError):
            duration.parse('-23.5')

    def test_simple_units(self):
        self.assertEqual(duration.parse('1s'), 1)
        self.assertEqual(duration.parse('1 s'), 1)
        self.assertEqual(duration.parse('1 sec'), 1)
        self.assertEqual(duration.parse('2 seconds'), 2)
        self.assertEqual(duration.parse('2 seconds'), 2)

    def test_simple_failure(self):
        with self.assertRaises(ValueError):
            duration.parse('1ss')

        with self.assertRaises(ValueError):
            duration.parse('1secondss')

        with self.assertRaises(ValueError):
            duration.parse('1milisecond')

        with self.assertRaises(ValueError):
            duration.parse('1 killosecond')

        with self.assertRaises(ValueError):
            duration.parse('1 milliwombat')

        with self.assertRaises(ValueError):
            duration.parse('')

    def test_complex(self):
        self.assertEqual(duration.parse('2 hours, 3 minutes, 3.5 seconds'),
                         2 * 60 * 60 + 3 * 60 + 3.5)
        self.assertEqual(duration.parse('2 hours, 3 minutes, 3.5 picoseconds'),
                         2 * 60 * 60 + 3 * 60 + 3.5 * 10 ** -12)
        self.assertEqual(duration.parse('2hrs, 3 minutes, 3.5ps'),
                         2 * 60 * 60 + 3 * 60 + 3.5 * 10 ** -12)

    def test_complex_failure(self):
        with self.assertRaises(ValueError):
            duration.parse('2 hourses, 3 minutes, 3.5 seconds')

        with self.assertRaises(ValueError):
            duration.parse('2 hours minutes, 3 minutes, 3.5 seconds')

        with self.assertRaises(ValueError):
            duration.parse('2 3 hours, 3 minutes, 3.5 seconds')

        with self.assertRaises(ValueError):
            duration.parse('hours, 3 minutes, 3.5 seconds')

        with self.assertRaises(ValueError):
            duration.parse('3 hours, 3 minutes, 3.5')
