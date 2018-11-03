import unittest
from bibliopixel.drivers.channel_order import ChannelOrder

make = ChannelOrder.make


class ChannelOrderTest(unittest.TestCase):
    def test_all(self):
        self.assertIs(make('rgb'), ChannelOrder.RGB)
        self.assertIs(make(0), ChannelOrder.RGB)
        self.assertIs(make([0, 1, 2]), ChannelOrder.RGB)

        self.assertIs(make('gRB'), ChannelOrder.GRB)
        self.assertIs(make(2), ChannelOrder.GRB)
        self.assertIs(make((1, 0, 2)), ChannelOrder.GRB)

        self.assertIs(make('BGR'), ChannelOrder.BGR)
        self.assertIs(make(5), ChannelOrder.BGR)
        self.assertIs(make((2, 1, 0)), ChannelOrder.BGR)

    def test_index(self):
        self.assertIs(make(-1), ChannelOrder.BGR)
        self.assertIs(make(6), ChannelOrder.RGB)

        with self.assertRaises(TypeError):
            make(2.3)

    def test_fail(self):
        with self.assertRaisesRegex(ValueError, 'has non-rgb elements'):
            make('rxb')
        with self.assertRaisesRegex(ValueError, 'has members not between'):
            make([0, -1, 1])
        with self.assertRaisesRegex(ValueError, 'has duplicate elements'):
            make([0, 2, 2])
