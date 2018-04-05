import numpy, unittest
from numpy import array_equal

from bibliopixel.util import color_list, colors, log

COLORS1 = [colors.Red, colors.Green, colors.Blue, colors.White]
COLORS2 = [colors.Black, colors.Blue, colors.Red, colors.Black]
SUM12 = [colors.Red, colors.Cyan, colors.Magenta, colors.White]
WHITES = [colors.White, colors.White, colors.White, colors.White]
BLACKS = [colors.Black, colors.Black, colors.Black, colors.Black]


def array(cl):
    return numpy.array(cl, dtype='uint8')


def make_list(cl):
    return color_list.ColorList(cl[:])


def make_numpy(cl):
    return color_list.ColorList(array(cl))


class TestBase(unittest.TestCase):
    def assert_list_equal(self, actual, expected):
        x, y = actual.color_list, expected
        if isinstance(x, color_list.numpy_array):
            equals = array_equal(x, array(y))
        else:
            equals = (x == y)
        if not equals:
            log.printer('____')
            log.printer(x)
            log.printer('NOT EQUAL')
            log.printer(y)
            log.printer('____')
        self.assertTrue(equals)


class ColorListTest(TestBase):
    def assert_list_equal(self, actual, expected):
        x, y = actual.color_list, expected
        if isinstance(x, color_list.numpy_array):
            equals = array_equal(x, array(y))
        else:
            equals = (x == y)
        if not equals:
            log.printer('NOT EQUAL')
            log.printer(x)
            log.printer(y)
        self.assertTrue(equals)

    def test_simple(self):
        self.assertIs(numpy, color_list.numpy)
        self.assertIs(numpy.ndarray, color_list.numpy_array)

        cl = make_list([])
        self.assertIs(cl.math, color_list.ListMath)

        cl = make_numpy([])
        self.assertIs(cl.math, color_list.NumpyMath)

    def test_lists(self):
        cl1 = make_list(COLORS1)
        cl2 = make_list(COLORS2)
        cl1.add(cl2.color_list, 0)
        self.assert_list_equal(cl1, COLORS1)
        cl1.add(cl2.color_list, 1)
        self.assert_list_equal(cl1, SUM12)

    def test_numpy(self):
        cl1 = make_numpy(COLORS1)
        cl2 = make_numpy(COLORS2)
        cl1.add(cl2.color_list, 0)
        self.assert_list_equal(cl1, COLORS1)
        cl1.add(cl2.color_list, 1)
        self.assertTrue(cl1, SUM12)

    def test_clear_list(self):
        cl = make_list(COLORS1)
        cl.clear()
        self.assert_list_equal(cl, BLACKS)

    def test_clear_numpy(self):
        cl = make_numpy(COLORS1)
        cl.clear()
        self.assert_list_equal(cl, BLACKS)

    def test_copy_list(self):
        cl = make_list(COLORS1)
        cl = make_numpy(COLORS1)
        cl.copy_from(array(COLORS2))
        self.assert_list_equal(cl, COLORS2)

    def test_copy_numpy(self):
        cl = make_numpy(COLORS1)
        cl.copy_from(array(COLORS2))
        self.assert_list_equal(cl, COLORS2)


class MixerTest(TestBase):
    def do_test(self, mixer, thirds):
        self.assertEqual(mixer.levels, [0, 0, 0])
        self.assert_list_equal(mixer.color_list, COLORS1)

        mixer.mix()
        self.assert_list_equal(mixer.color_list, COLORS1)

        mixer.clear()
        mixer.mix()

        self.assert_list_equal(mixer.color_list, BLACKS)

        mixer.levels[:] = [1, 0, 0]
        mixer.clear()
        mixer.mix()
        self.assert_list_equal(mixer.color_list, COLORS2)

        mixer.levels[:] = [0, 1, 0]
        mixer.clear()
        mixer.mix()
        self.assert_list_equal(mixer.color_list, WHITES)

        mixer.levels[:] = [0, 0, 1]
        mixer.clear()
        mixer.mix()
        self.assert_list_equal(mixer.color_list, BLACKS)

        mixer.levels[:] = [1 / 3, 1 / 3, 1 / 3]
        mixer.clear()
        mixer.mix()
        self.assert_list_equal(mixer.color_list, thirds)

        mixer.levels[:] = [1, 1, 1]
        mixer.clear()
        mixer.mix(1 / 3)
        self.assert_list_equal(mixer.color_list, thirds)

    def test_lists(self):
        mixer = color_list.Mixer(COLORS1[:], [COLORS2, WHITES, BLACKS])
        self.do_test(mixer,
                     [(85, 85, 85), (85, 85, 170), (170, 85, 85), (85, 85, 85)])

    def test_numpy(self):
        mixer = color_list.Mixer(
            array(COLORS1), [array(COLORS2), array(WHITES), array(BLACKS)])
        self.do_test(mixer,
                     [(85, 85, 85), (85, 85, 170), (170, 85, 85), (85, 85, 85)])


del TestBase
