import copy, unittest
from bibliopixel.project import fill, merge, project
from bibliopixel.animation.sequence import Sequence
from bibliopixel.animation.matrix import BaseMatrixAnim
from bibliopixel.animation.off import OffAnim
from bibliopixel.layout import Cube, Matrix, Strip

BASE = {
    'animation': {
        'run': {},
        'datatype': OffAnim,
        'name': 'Off',
    },
    'controls': [],
    'drivers': [{'typename': 'simpixel'}],
    'layout': {},
    'maker': {'typename': 'bibliopixel.project.data_maker.Maker'},
    'path': '',
    'typename': 'bibliopixel.project.project.Project',
}


def fill_before(desc):
    desc = merge.merge(
        merge.DEFAULT_PROJECT, {'animation': {'typename': 'off'}}, desc)
    return project.Project.pre_recursion(desc)


def fill_after(desc):
    desc = merge.merge(merge.DEFAULT_PROJECT, desc)
    desc['layout'] = desc['layout'] or fill.fill_layout(desc['animation'])
    return desc


class FillTest(unittest.TestCase):
    def test_both(self):
        actual = fill_before({'layout': 'matrix'})
        expected = dict(BASE, layout={'typename': 'matrix'})
        self.assertEqual(actual, expected)

    def test_drivers_empty(self):
        self.assertEqual(fill_before({}), BASE)

    def test_drivers_one(self):
        actual = fill_before({'driver': 'lpd8806'})
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
        actual = fill_after(copy.deepcopy(source))
        expected = {
            'aliases': {'bpa': 'BiblioPixelAnimations'},
            'shape': (),
            'driver': {},
            'drivers': [],
            'layout': {
                'width': 23,
                'height': 32,
                'datatype': Matrix,
            },
            'numbers': 'python',
            'palettes': {},
            'run': {},
        }
        expected = dict(source, **expected)
        self.assertEqual(actual, dict(BASE, **expected))

    def test_1_dimension(self):
        source = {'shape': 3}
        actual = fill_before(source)
        expected = {
            'drivers': [{'num': 3, 'typename': 'simpixel'}],
            'layout': {'datatype': Strip},
        }
        self.assertEqual(actual, dict(BASE, **expected))

        source = {'shape': [3]}
        actual = fill_before(source)
        self.assertEqual(actual, dict(BASE, **expected))

    def test_2_shape(self):
        source = {'shape': [2, 5]}
        actual = fill_before(source)
        expected = {
            'drivers': [{'num': 10, 'typename': 'simpixel'}],
            'layout': {'datatype': Matrix, 'width': 2, 'height': 5},
        }
        self.assertEqual(actual, dict(BASE, **expected))

    def test_3_shape(self):
        source = {'shape': [2, 3, 7]}
        actual = fill_before(source)
        expected = {
            'drivers': [{'num': 42, 'typename': 'simpixel'}],
            'layout': {'datatype': Cube, 'x': 2, 'y': 3, 'z': 7},
        }
        self.assertEqual(actual, dict(BASE, **expected))
