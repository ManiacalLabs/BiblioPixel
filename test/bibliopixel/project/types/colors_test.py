from . base import TypesBaseTest
from bibliopixel.util import colors


class ColorTypesTest(TypesBaseTest):
    def test_empty(self):
        self.make('colors', [], [])

    def test_single(self):
        self.make('colors', ['red'], [(255, 0, 0)])
        self.make('colors', 'red', [(255, 0, 0)])

    def test_many(self):
        self.make('colors', ['red', [0, 255, 0], 127],
                  [(255, 0, 0), (0, 255, 0), (127, 127, 127)])

    def test_1d_list(self):
        self.make('colors', [0, 255, 0, 255, 0, 0, 23, 17],
                  [(0, 255, 0), (255, 0, 0)])
