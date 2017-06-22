import unittest
from bibliopixel.layout.geometry import segment


class SegmentTest(unittest.TestCase):
    def test_all(self):
        segments = segment.make_segments(list(range(21)), 3)
        self.assertEqual(len(segments), 7)
        for i, s in enumerate(segments):
            self.assertEqual(len(s), 3)
            for j, v in enumerate(s):
                self.assertEqual(v, 3 * i + j)
