import unittest
from bibliopixel.control.address import Address


class AddressTest(unittest.TestCase):

    def test_empty(self):
        address = Address('')
        self.assertFalse(address)
        self.assertFalse(address.segments)
        self.assertFalse(address.assignment)
        self.assertEqual(address.get(23), 23)
        with self.assertRaises(ValueError):
            address.set(self, 23)

    def test_attrib(self):
        address = Address('attr')
        self.assertEqual(len(address.segments), 1)
        self.attr = 'bingo'
        self.assertIs(address.get(self), 'bingo')
        address.set(self, 'bang')
        self.assertIs(address.get(self), 'bang')

    def test_attrib_error(self):
        address = Address('.attr')
        with self.assertRaises(AttributeError):
            address.get(AddressTest)

        with self.assertRaises(AttributeError):
            address.get(0)

    def test_array(self):
        address = Address('[1]')
        self.assertEqual(len(address.segments), 1)
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

        address = Address('.attr1[0][test][1][heck].attr2.attr3')
        self.assertEqual(len(address.segments), 7)
        self.assertEqual(address.get(self), 'bingo')
        address.set(self, 'bang')
        self.assertEqual(self.attr3, 'bang')

    def call(self, x):
        self.call_result = 23

    def test_trivial_call(self):
        address = Address('()')
        self.assertEqual(len(address.segments), 1)
        result = []

        address.set(result.append, 'value')
        self.assertEqual(result, ['value'])

    def test_call(self):
        address = Address('.call()')
        self.assertEqual(len(address.segments), 2)
        address.set(self, 23)
        self.assertEqual(self.call_result, 23)

    def call2(self):
        return None, lambda: self

    def test_call_complex(self):
        self.results = []
        address = Address('.call2()[1]().call()')
        self.assertEqual(len(address.segments), 6)
        address.set(self, 23)
        self.assertEqual(self.call_result, 23)

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

    def test_assignment(self):
        self.attr = None
        Address('.attr = 1').set(self)
        self.assertEqual(self.attr, 1)

        self.attr = None
        Address('.attr = 1, 2.5, 3').set(self)
        self.assertEqual(self.attr, (1, 2.5, 3))
