import copy, unittest
from bibliopixel.project import project2
from bibliopixel.animation.sequence import Sequence
from bibliopixel.animation.matrix import BaseMatrixAnim
from bibliopixel.layout import Matrix
from bibliopixel.project.data_maker import Maker


def classname(c):
    return '%s.%s' % c.__module__, c.__name__


class Project2Test(unittest.TestCase):
    def test_empty(self):
        with self.assertRaises(ValueError):
            project2.project()

    def test_single(self):
        source = {
            'animation': {
                'typename': 'bibliopixel.animation.matrix.BaseMatrixAnim',
                'width': 23,
                'height': 32,
            }
        }
        project = project2.project(source)
        self.assertEquals(
            [BaseMatrixAnim, 1, Matrix, Maker, 23, 32],
            [
                type(project.animation),
                len(project.drivers),
                type(project.layout),
                type(project.maker),
                project.layout.width,
                project.layout.height,
            ])
