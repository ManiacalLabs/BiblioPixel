import unittest
from bibliopixel.project import merge

BASE = dict(
    merge.DEFAULT_PROJECT,
    maker={'typename': 'bibliopixel.project.data_maker.Maker'},
    run={},
)


class MergeTest(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(merge.merge(), {})

    def test_single(self):
        self.assertEqual(merge.merge(merge.DEFAULT_PROJECT), BASE)

    def test_more(self):
        result = merge.merge(
            merge.DEFAULT_PROJECT,
            {
                'animation': 'foo',
                'driver': 'bar',
                'drivers': ['bang', 'bop'],
            },
            {
                'animation': 'bfoo',
                'maker': {'numpy_dtype': 'float'},
                'path': 'path/to/dir'
            })
        expected = {
            'aliases': {'bpa': 'BiblioPixelAnimations'},
            'animation': {'typename': 'bfoo'},
            'controls': [],
            'shape': (),
            'driver': {'typename': 'bar'},
            'drivers': ['bang', 'bop'],
            'layout': {},
            'numbers': 'python',
            'maker': {
                'numpy_dtype': 'float',
                'typename': 'bibliopixel.project.data_maker.Maker'
            },
            'palettes': {},
            'path': 'path/to/dir',
            'run': {},
            'typename': 'bibliopixel.project.project.Project'
        }

        self.assertEqual(result, expected)
