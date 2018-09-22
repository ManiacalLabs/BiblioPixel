import unittest
from bibliopixel.layout import cutter


class MockLayout:
    def __init__(self, color_list, width, height):
        self.results = []
        self.color_list = list(color_list)
        self.width = width
        self.height = height

    def get(self, column, row):
        return self.color_list[self.width * row + column]

    def set(self, column, row, color):
        self.color_list[column + self.width * row] = color


class CutterTest(unittest.TestCase):
    def assert_cut(self, expected_slices, expected_result,
                   by_row=True, width=3, height=2, color_list='abcdef'):
        layout = MockLayout(color_list, width, height)
        cutter = self.maker(layout, by_row)
        slices = []

        def function(value):
            slices.append(''.join(value))
            value.append(value.pop(0))

        cutter.apply(function)
        result = ''.join(layout.color_list)
        self.assertEqual(expected_slices, slices)
        self.assertEqual(expected_result, result)

    def test_get_row(self):
        self.assert_cut(['abc', 'def'], 'bcaefd')

    def test_get_column(self):
        self.assert_cut(['ad', 'be', 'cf'], 'defabc', by_row=False)


class SlicerTest(CutterTest):
    maker = cutter.Slicer


class IndexerTest(CutterTest):
    maker = cutter.Indexer


del CutterTest
