import unittest
from bibliopixel.controllers.address import Address


class AddressTest(unittest.TestCase):

    def test_empty_error(self):
        with self.assertRaises(ValueError) as e:
            Address('')
        print(dir(e.exception))
        self.assertIn('Empty Address', e.exception.args[0])

    def test_attrib(self):
        address = Address('attr')
        self.assertEqual(len(address.address), 1)
        self.attr = 'bingo'
        self.assertIs(address.get(self), 'bingo')
        address.set(self, 'bang')
        self.assertIs(address.get(self), 'bang')

    def test_attrib_error(self):
        address = Address('attr')
        with self.assertRaises(AttributeError):
            address.get(AddressTest)

        with self.assertRaises(AttributeError):
            address.get(0)

    def test_array(self):
        address = Address('[1]')
        self.assertEqual(len(address.address), 1)
        data = [2, 4, 6]
        self.assertEqual(address.get(data), 4)
        address.set(data, 3)
        self.assertEqual(data, [2, 3, 6])

    def test_array_error(self):
        address = Address('[1]')
        with self.assertRaises(IndexError):
            address.get([0])

        with self.assertRaises(IndexError):
            address.set([0], 5)

        with self.assertRaises(TypeError):
            address.get(0)

    def test_compound(self):
        self.attr1 = [{'test': [None, {'heck': self}]}, 'x', 'y']
        self.attr2 = self
        self.attr3 = 'bingo'

        address = Address('attr1[0][test][1][heck].attr2.attr3')
        self.assertEqual(len(address.address), 7)
        self.assertEqual(address.get(self), 'bingo')
        address.set(self, 'bang')
        self.assertEqual(self.attr3, 'bang')

    def test_compound_error(self):
        address = Address('attr1[0][test][1][heck].attr2.attr3')

        with self.assertRaises(AttributeError):
            address.get(self)

        self.attr1 = None
        with self.assertRaises(TypeError):
            address.get(self)

        with self.assertRaises(TypeError):
            address.set(self, 2)

    def test_segment_start_with_index(self):
        Address('[1]')
        with self.assertRaises(ValueError):
            Address('foo.[1]')
