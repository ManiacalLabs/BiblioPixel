from . base import TypesBaseTest
from bibliopixel import colors


class ColorTypesTest(TypesBaseTest):
    def test_empty(self):
        self.make('colors', [], [])

    def test_single(self):
        self.make('colors', ['red'], [(255, 0, 0)])

    def test_many(self):
        self.make('colors', ['red', [0, 255, 0], 127],
                  [(255, 0, 0), (0, 255, 0), (127, 127, 127)])
