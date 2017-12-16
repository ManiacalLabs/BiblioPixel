import copy, unittest
from bibliopixel.project import cleanup, merge, project
from bibliopixel.animation.sequence import Sequence
from bibliopixel.animation.matrix import BaseMatrixAnim
from bibliopixel.animation.off import OffAnim
from bibliopixel.layout import Cube, Matrix, Strip

BASE = {
    'animation': {
        'run': {},
        'datatype': OffAnim,
        'typename': 'off',
    },
    'drivers': [{'typename': 'simpixel'}],
    'layout': {},
    'maker': {'typename': 'bibliopixel.project.data_maker.Maker'},
    'path': '',
    'typename': 'bibliopixel.project.project.Project',
}


def cleanup_before(desc):
    desc = merge.merge(
        merge.DEFAULT_PROJECT, {'animation': {'typename': 'off'}}, desc)
    return project.Project.pre_recursion(desc)


def cleanup_after(desc):
    desc = merge.merge(merge.DEFAULT_PROJECT, desc)
    desc['layout'] = desc['layout'] or cleanup.cleanup_layout(desc['animation'])
    return desc


class CleanupTest(unittest.TestCase):
    def test_both(self):
        actual = cleanup_before({'layout': 'matrix'})
        expected = dict(BASE, layout={'typename': 'matrix'})
        self.assertEqual(actual, expected)

    def test_drivers_empty(self):
        self.assertEqual(cleanup_before({}), BASE)

    def test_drivers_one(self):
        actual = cleanup_before({'driver': 'lpd8806'})
        expected = dict(BASE, drivers=[{'typename': 'lpd8806'}])
        self.assertEqual(actual, expected)

    def test_layout(self):
        source = {
            'animation': {
                'datatype': BaseMatrixAnim,
                'width': 23,
                'height': 32,
                'wombat': 7,
            },
        }
        actual = cleanup_after(copy.deepcopy(source))
        expected = {
            'aliases': {},
            'dimensions': (),
            'driver': {},
            'drivers': [],
            'layout': {
                'width': 23,
                'height': 32,
                'datatype': Matrix,
            },
            'run': {},
        }
        expected = dict(source, **expected)
        self.assertEqual(actual, dict(BASE, **expected))

    def test_1_dimension(self):
        source = {'dimensions': 3}
        actual = cleanup_before(source)
        expected = {
            'drivers': [{'num': 3, 'typename': 'simpixel'}],
            'layout': {'datatype': Strip},
        }
        self.assertEqual(actual, dict(BASE, **expected))

        source = {'dimensions': [3]}
        actual = cleanup_before(source)
        self.assertEqual(actual, dict(BASE, **expected))

    def test_2_dimensions(self):
        source = {'dimensions': [2, 5]}
        actual = cleanup_before(source)
        expected = {
            'drivers': [{'num': 10, 'typename': 'simpixel'}],
            'layout': {'datatype': Matrix, 'width': 2, 'height': 5},
        }
        self.assertEqual(actual, dict(BASE, **expected))

    def test_3_dimensions(self):
        source = {'dimensions': [2, 3, 7]}
        actual = cleanup_before(source)
        expected = {
            'drivers': [{'num': 42, 'typename': 'simpixel'}],
            'layout': {'datatype': Cube, 'x': 2, 'y': 3, 'z': 7},
        }
        self.assertEqual(actual, dict(BASE, **expected))
