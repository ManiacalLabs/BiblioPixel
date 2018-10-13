import unittest
from fractions import Fraction
from bibliopixel.util import log
from bibliopixel.control.envelope import segments


class SegmentsTest(unittest.TestCase):
    def test_empty_segments(self):
        segs = segments.Segments()
        expected = []
        function_tester(segs, self, expected)

        expected = [0, 0, 0, 0]
        function_tester(segs, self, expected)

    def test_simple_segments(self):
        segs = segments.Segments([1, 2, 3, 4])
        self.assertEqual(segs.total_time, 1)

        expected = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]
        function_tester(segs, self, expected)

    def test_simple_segments2(self):
        segs = segments.Segments([1, 1.5, 3, 7])
        self.assertEqual(segs.total_time, 1)

        expected = [0, 0.5, 1, 1.25, 1.5, 2.25, 3, 5, 7]
        function_tester(segs, self, expected)

    def test_decreasing_segments(self):
        segs = segments.Segments([1, 3, 2, 4])
        self.assertEqual(segs.total_time, 1)

        expected = [0, 0.5, 1, 2, 3, 2.5, 2, 3, 4]
        function_tester(segs, self, expected)

    def test_timed_segments(self):
        segs = segments.Segments([(1, 1), (2, 1), (5, 0.5), (11, 0.5)])
        self.assertEqual(segs.total_time, 3)
        log.printer(segs)
        self.assertEqual(segs(0), 0)
        self.assertEqual(segs(0.5), 0.5)
        self.assertEqual(segs(1), 1)
        self.assertEqual(segs(2), 2)
        self.assertEqual(segs(2.25), 3.5)
        self.assertEqual(segs(2.5), 5)
        self.assertEqual(segs(2.75), 8)
        self.assertEqual(segs(3), 11)


def function_tester(function, test, expected, frac=0):
    n = len(expected)
    frac = frac or (n - 1)
    actual = [function(Fraction(i, frac)) for i in range(n)]

    actual = [round(i, 12) for i in actual]
    expected = [round(i, 12) for i in expected]
    test.assertEqual(expected, actual)
