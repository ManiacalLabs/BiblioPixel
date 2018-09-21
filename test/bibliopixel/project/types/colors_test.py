from . base import TypesBaseTest
from bibliopixel.util.colors.palette import Palette


class ColorTypesTest(TypesBaseTest):
    def test_empty(self):
        self.make('colors', [], Palette())

    def test_single(self):
        self.make('colors', ['red'], Palette([(255, 0, 0)]))
        self.make('colors', 'red', Palette([(255, 0, 0)]))

    def test_many(self):
        self.make('colors', ['red', [0, 255, 0], 127],
                  Palette([(255, 0, 0), (0, 255, 0), (127, 127, 127)]))

    def test_1d_list(self):
        self.make('colors', [0, 255, 0, 255, 0, 0, 23, 17],
                  Palette([(0, 255, 0), (255, 0, 0)]))

    def test_dict(self):
        data = {
            'colors': [0, 255, 0, 255, 0, 0, 23, 17, 5],
            'scale': 2,
            'serpentine': True}

        expected = Palette(
            colors=[(0, 255, 0), (255, 0, 0), (23, 17, 5)],
            scale=2,
            serpentine=True)

        self.make('colors', data, expected)
