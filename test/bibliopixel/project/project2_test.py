import copy, unittest
from bibliopixel.project import project
from bibliopixel.animation.sequence import Sequence
from bibliopixel.animation.matrix import BaseMatrixAnim
from bibliopixel.layout import Matrix
from bibliopixel.project.data_maker import Maker


def classname(c):
    return '%s.%s' % c.__module__, c.__name__


class Project2Test(unittest.TestCase):
    def test_empty(self):
        with self.assertRaises(ValueError):
            project.project()

    def test_single(self):
        source = {
            'animation': {
                'typename': 'bibliopixel.animation.matrix.BaseMatrixAnim',
                'width': 23,
                'height': 32,
            }
        }
        pr = project.project(source)
        self.assertEquals(
            [BaseMatrixAnim, 1, Matrix, Maker, 23, 32],
            [
                type(pr.animation),
                len(pr.drivers),
                type(pr.layout),
                type(pr.maker),
                pr.layout.width,
                pr.layout.height,
            ])
