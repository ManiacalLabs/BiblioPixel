import unittest
from bibliopixel.util import offset_range


class OffsetRangeTest(unittest.TestCase):
    def test_empty(self):
        dmx = offset_range.DMXChannel.make()

        self.assertEqual(dmx.index(0), None)
        self.assertEqual(dmx.index(1), 0)
        self.assertEqual(dmx.index(2), 1)
        self.assertEqual(dmx.index(511), 510)
        self.assertEqual(dmx.index(512), 511)
        self.assertEqual(dmx.index(513), None)

        l256 = list(range(256))
        r = list(dmx.read_from(l256))
        self.assertEqual(r, l256 + ([0] * 256))

        target = [23] * 128
        dmx.copy_to(l256, target)
        self.assertEqual(target, list(range(128)))

    def test_empty_copy(self):
        dmx = offset_range.DMXChannel.make()

        l256 = list(range(256))
        r = list(dmx.read_from(l256))
        self.assertEqual(r, l256 + ([0] * 256))

        target = []
        dmx.copy_to(l256, target)
        self.assertEqual(target, [])

    def test_positive_offset(self):
        midi = offset_range.MidiChannel(offset=4)
        self.assertEqual(midi.index(0), None)
        self.assertEqual(midi.index(1), None)
        self.assertEqual(midi.index(4), None)
        self.assertEqual(midi.index(5), 0)
        self.assertEqual(midi.index(6), 1)
        self.assertEqual(midi.index(15), 10)
        self.assertEqual(midi.index(16), 11)
        self.assertEqual(midi.index(16), 11)
        self.assertEqual(midi.index(17), None)

        expected = [-1, -1, -1, -1] + list(range(12))
        actual = list(midi.read_from(range(16), pad=-1))
        self.assertEqual(expected, actual)

        target = [100] * 100
        midi.copy_to(list(range(16)), target)
        expected = list(range(4, 16)) + [100] * 88
        self.assertEqual(target, expected)

    def test_negative_offset(self):
        midi = offset_range.MidiChannel(-4)
        self.assertEqual(midi.index(0), None)
        self.assertEqual(midi.index(1), 4)
        self.assertEqual(midi.index(2), 5)
        self.assertEqual(midi.index(12), 15)
        self.assertEqual(midi.index(13), None)

        actual = list(midi.read_from(range(16), pad=-1))
        expected = list(range(4, 16)) + [-1, -1, -1, -1]
        self.assertEqual(expected, actual)

        target = [100] * 8
        midi.copy_to(list(range(16)), target)

        expected = [4, 5, 6, 7, 8, 9, 10, 11]
        self.assertEqual(target, expected)

    def test_begin_end_offset(self):
        midi = offset_range.MidiChannel(offset=-5, begin=6, end=8)
        self.assertEqual(midi.index(0), None)
        self.assertEqual(midi.index(4), None)
        self.assertEqual(midi.index(5), None)
        self.assertEqual(midi.index(6), 10)
        self.assertEqual(midi.index(7), 11)
        self.assertEqual(midi.index(8), 12)
        self.assertEqual(midi.index(9), None)
        self.assertEqual(midi.index(10), None)

        actual = list(midi.read_from(range(16)))
        expected = [0, 0, 0, 0, 0, 10, 11, 12, 0, 0, 0, 0, 0, 0, 0, 0]

        self.assertEqual(expected, actual)

        target = [100] * 24
        midi.copy_to(list(range(7)), target)
        expected = 5 * [100] + [5, 6] + 17 * [100]
        self.assertEqual(target, expected)

        target = [100] * 24
        midi.copy_to(list(range(8)), target)
        expected = 5 * [100] + [5, 6, 7] + 16 * [100]
        self.assertEqual(target, expected)

        target = [100] * 24
        midi.copy_to(list(range(9)), target)
        expected = 5 * [100] + [5, 6, 7] + 16 * [100]
        self.assertEqual(target, expected)

    def test_errors(self):
        with self.assertRaises(ValueError):
            offset_range.MidiChannel(begin=0)

        offset_range.MidiChannel(begin=1)
        offset_range.MidiChannel(begin=16)

        with self.assertRaises(ValueError):
            offset_range.MidiChannel(begin=17)

        with self.assertRaises(ValueError):
            offset_range.MidiChannel(end=0)

        offset_range.MidiChannel(end=1)
        offset_range.MidiChannel(end=16)

        with self.assertRaises(ValueError):
            offset_range.MidiChannel(end=17)

        with self.assertRaises(ValueError):
            offset_range.MidiChannel(begin=2, end=1)
