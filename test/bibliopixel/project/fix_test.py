import copy, unittest
from bibliopixel.project import fix
from bibliopixel.animation.sequence import Sequence
from bibliopixel.animation.matrix import BaseMatrixAnim
from bibliopixel.layout import Matrix


def fix_drivers(desc):
    fix.fix_drivers(desc)
    return desc


def fix_layout(desc):
    fix.fix_layout_and_animation(desc)
    return desc


class FixTest(unittest.TestCase):
    def test_both(self):
        actual = fix_drivers({'layout': 'matrix', 'drivers': []})
        expected = {'layout': 'matrix', 'drivers': fix.DEFAULT_DRIVERS}
        self.assertEqual(actual, expected)

    def test_drivers_empty(self):
        self.assertEqual(
            fix_drivers({}),
            {'drivers': fix.DEFAULT_DRIVERS})

    def test_drivers_one(self):
        self.assertEqual(
            fix_drivers({'driver': 'lpd8806'}),
            {'drivers': [{'typename': 'lpd8806'}]})

    def test_layout(self):
        source = {
            'drivers': [{}],
            'run_animation': {
                'animation': {
                    'datatype': BaseMatrixAnim,
                    'width': 23,
                    'height': 32,
                    'wombat': 7,
                },
                'run': {},
            }
        }
        actual = fix_layout(copy.deepcopy(source))
        expected = dict(
            source, layout={'datatype': Matrix, 'width': 23, 'height': 32})
        self.assertEqual(actual, expected)
