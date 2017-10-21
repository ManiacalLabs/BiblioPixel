import unittest
from bibliopixel.project import merge

BASE = dict(
    merge.DEFAULT_PROJECT,
    maker={'typename': 'bibliopixel.project.data_maker.Maker'})


class MergeTest(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(merge.merge(), BASE)

    def test_more(self):
        result = merge.merge(
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
            'animation': {'typename': 'bfoo'},
            'driver': {'typename': 'bar'},
            'drivers': ['bang', 'bop'],
            'layout': {},
            'maker': {
                'numpy_dtype': 'float',
                'typename': 'bibliopixel.project.data_maker.Maker'
            },
            'path': 'path/to/dir',
            'run': {},
            'typename': 'bibliopixel.project.project2.Project'
        }

        self.assertEqual(result, expected)
