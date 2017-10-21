import copy, unittest
from bibliopixel.project.fix import fix_drivers, fix_layout, DEFAULT_DRIVERS
from bibliopixel.animation.sequence import Sequence
from bibliopixel.animation.matrix import BaseMatrixAnim
from bibliopixel.layout import Matrix


class FixTest(unittest.TestCase):
    def test_both(self):
        actual = fix_drivers(fix_layout({'layout': 'matrix', 'drivers': []}))
        expected = {'layout': 'matrix', 'drivers': DEFAULT_DRIVERS}
        self.assertEqual(actual, expected)

    def test_drivers_empty(self):
        self.assertEqual(
            fix_drivers({}),
            {'drivers': DEFAULT_DRIVERS})

    def test_drivers_one(self):
        self.assertEqual(
            fix_drivers({'driver': 'lpd8806'}),
            {'drivers': [{'typename': 'lpd8806'}]})

    def test_layout(self):
        source = {
            'drivers': [{}],
            'animation': {
                'datatype': BaseMatrixAnim,
                'width': 23,
                'height': 32,
                'wombat': 7,
            }
        }
        actual = fix_layout(copy.deepcopy(source))
        expected = dict(
            source, layout={'datatype': Matrix, 'width': 23, 'height': 32})
        self.assertEqual(actual, expected)
