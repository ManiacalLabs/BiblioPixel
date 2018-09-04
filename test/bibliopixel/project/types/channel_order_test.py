from . base import TypesBaseTest
from bibliopixel.drivers import channel_order


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

        with self.assertRaises(ValueError):
            self.make('c_order', [1, 2])
