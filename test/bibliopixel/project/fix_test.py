import copy, unittest
from bibliopixel.project import merge, project
from bibliopixel.animation.sequence import Sequence
from bibliopixel.animation.matrix import BaseMatrixAnim
from bibliopixel.animation.off import OffAnim
from bibliopixel.layout import Matrix

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


def fix_before(desc):
    desc = merge.merge(
        merge.DEFAULT_PROJECT, {'animation': {'typename': 'off'}}, desc)
    return project.Project.pre_recursion(desc)


def fix_after(desc):
    desc = merge.merge(merge.DEFAULT_PROJECT, desc)
    desc['layout'] = desc['layout'] or project.fix_layout(desc['animation'])
    return desc


class FixTest(unittest.TestCase):
    def test_both(self):
        actual = fix_before({'layout': 'matrix'})
        expected = dict(BASE, layout={'typename': 'matrix'})
        self.assertEqual(actual, expected)

    def test_drivers_empty(self):
        self.assertEqual(fix_before({}), BASE)

    def test_drivers_one(self):
        actual = fix_before({'driver': 'lpd8806'})
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
        actual = fix_after(source)
        expected = {
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
