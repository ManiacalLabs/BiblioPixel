import copy, unittest
from bibliopixel.project import defaults, project
from bibliopixel.animation.sequence import Sequence
from bibliopixel.animation.matrix import BaseMatrixAnim
from bibliopixel.layout import Matrix
from bibliopixel.project.data_maker import Maker
from test.bibliopixel import patch


def classname(c):
    return '%s.%s' % c.__module__, c.__name__


class Project2Test(unittest.TestCase):
    def test_empty(self):
        with patch.patch(defaults, 'BYPASS_PROJECT_DEFAULTS', True):
            project.project()

    def test_single(self):
        source = {
            'animation': {
                'typename': 'bibliopixel.animation.matrix.BaseMatrixAnim',
                'width': 23,
                'height': 32,
            }
        }
        with patch.patch(defaults, 'BYPASS_PROJECT_DEFAULTS', True):
            pr = project.project(source)

        self.assertEqual(
            [BaseMatrixAnim, 1, Matrix, Maker, 23, 32],
            [
                type(pr.animation),
                len(pr.drivers),
                type(pr.layout),
                type(pr.maker),
                pr.layout.width,
                pr.layout.height,
            ])
