import numpy, numpy.testing, unittest

from bibliopixel.util import colors, color_list, log
from bibliopixel.util.color_list import check_numpy, ListMath, NumpyMath
from bibliopixel.util.colors.make import to_triplets

COLORS1 = [colors.Red, colors.Green, colors.Blue, colors.White]
COLORS2 = [colors.Black, colors.Blue, colors.Red, colors.Black]
SUM12 = [colors.Red, colors.Cyan, colors.Magenta, colors.White]
WHITES = [colors.White, colors.White, colors.White, colors.White]
BLACKS = [colors.Black, colors.Black, colors.Black, colors.Black]


def make_numpy(cl):
    return numpy.array(cl, dtype='float')


class TestBase:
    def assert_list_equal(self, actual, expected):
        x, y = actual, expected
        if hasattr(x, 'shape'):
            equals = numpy.array_equal(x, make_numpy(y))
        else:
            log.printer(type(x), type(y))
            equals = (x == y)
        if not equals:
            log.printer('____')
            log.printer(x)
            log.printer('NOT EQUAL')
            log.printer(y)
            log.printer('____')
        self.assertTrue(equals)


class ColorListTest(unittest.TestCase, TestBase):
    def test_simple(self):
        self.assertIs(numpy, color_list.numpy)

        self.assertFalse(color_list.is_numpy([]))
        self.assertTrue(color_list.is_numpy(make_numpy([])))

        self.assertIs(color_list.Math([]), ListMath)
        self.assertIs(color_list.Math(make_numpy([])), NumpyMath)

    def test_lists(self):
        cl1 = COLORS1[:]
        cl2 = COLORS2[:]
        ListMath.add(cl1, cl2, 0)
        self.assert_list_equal(cl1, COLORS1)
        ListMath.add(cl1, cl2)
        self.assert_list_equal(cl1, SUM12)

    def test_numpy(self):
        cl1 = make_numpy(COLORS1)
        cl2 = make_numpy(COLORS2)
        NumpyMath.add(cl1, cl2, 0)
        self.assert_list_equal(cl1, COLORS1)
        NumpyMath.add(cl1, cl2, 1)
        self.assert_list_equal(cl1, SUM12)

    def test_clear_list(self):
        cl = COLORS1[:]
        ListMath.clear(cl)
        self.assert_list_equal(cl, BLACKS)

        cl = []
        ListMath.clear(cl)
        self.assert_list_equal(cl, [])

    def test_clear_numpy(self):
        cl = make_numpy(COLORS1)
        NumpyMath.clear(cl)
        self.assert_list_equal(cl, BLACKS)
        self.assert_list_equal(cl, BLACKS)

    def test_copy_list(self):
        cl = COLORS1[:]
        ListMath.copy(cl, COLORS2)
        self.assert_list_equal(cl, COLORS2)

    def test_copy_numpy(self):
        cl = make_numpy(COLORS1)
        NumpyMath.copy(cl, make_numpy(COLORS2))
        self.assert_list_equal(cl, COLORS2)

    def test_sum_list(self):
        self.assertEqual(ListMath.sum(COLORS1), 6 * 255)

    def test_sum_numpy(self):
        self.assertEqual(NumpyMath.sum(make_numpy(COLORS1)), 6 * 255)

    def test_scale_list(self):
        cl = COLORS1[:]
        ListMath.scale(cl, 0.5)
        self.assert_list_equal(
            cl,
            [(127.5, 0.0, 0.0),
             (0.0, 127.5, 0.0),
             (0.0, 0.0, 127.5),
             (127.5, 127.5, 127.5)])

    def test_scale_numpy(self):
        cl = make_numpy(COLORS1)
        NumpyMath.scale(cl, 0.5)
        self.assert_list_equal(
            cl,
            [(127.5, 0.0, 0.0),
             (0.0, 127.5, 0.0),
             (0.0, 0.0, 127.5),
             (127.5, 127.5, 127.5)])


class MixerTest(unittest.TestCase, TestBase):
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
            make_numpy(COLORS1),
            [make_numpy(COLORS2), make_numpy(WHITES), make_numpy(BLACKS)])
        self.do_test(mixer,
                     [(85, 85, 85), (85, 85, 170), (170, 85, 85), (85, 85, 85)])


class ToTripletsTest(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(to_triplets(COLORS1), COLORS1)

    def test_numpy(self):
        cl = make_numpy(COLORS1)
        numpy.testing.assert_array_equal(to_triplets(cl), cl)

    def test_exact_count(self):
        cl = list(sum(COLORS1, ()))
        self.assertEqual(to_triplets(cl), COLORS1)

    def test_overage(self):
        cl = list(sum(COLORS1, ()))
        self.assertEqual(to_triplets(cl), COLORS1)

        cl.append(255)
        self.assertEqual(to_triplets(cl), COLORS1)

        cl.append(0)
        self.assertEqual(to_triplets(cl), COLORS1)

        cl.append(0)
        self.assertEqual(to_triplets(cl), COLORS1 + [colors.Red])


class CheckTest(unittest.TestCase):
    def test_works(self):
        self.color_list = make_numpy(COLORS1)
        check_numpy(self)
        check_numpy(self, 'name')

    def test_fails(self):
        self.color_list = []
        with self.assertRaises(ValueError):
            check_numpy(self)
        with self.assertRaises(ValueError):
            check_numpy(self, 'name')
