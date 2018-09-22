import collections, fractions, unittest
from bibliopixel.control import extractor

KEYS_BY_TYPE = {
    'note_on': ('channel', 'type', 'note', 'velocity'),
    'control_change': ('channel', 'type', 'control', 'value'),
    'pitchwheel': ('channel', 'type', 'pitch'),
}

NORMALIZERS = {
    'pitch': lambda x: fractions.Fraction(x - 8192) / 8192,
    'value': lambda x: fractions.Fraction(x) / 127,
    'velocity': lambda x: fractions.Fraction(x) / 127,
}

C3 = {'type': 'note_on', 'note': 32, 'channel': 1, 'velocity': 96}
C3_OFF = {'type': 'note_off', 'note': 32, 'channel': 1, 'velocity': 0, 'x': 47}

BC = {'type': 'control_change', 'channel': 2, 'control': 2, 'value': 10}
BC3 = {'type': 'control_change', 'channel': 3, 'control': 2, 'value': 128}
MOD = {'type': 'control_change', 'channel': 2, 'control': 1, 'value': 128}
PB = {'type': 'control_change', 'channel': 2, 'control': 1, 'value': 128}

OTHER = {'type': 'other', 'channel': 32, 'thing': 'stuff'}


class ExtractorTest(unittest.TestCase):
    def run_test(self, msg, expected, **kwds):
        md = extractor.Extractor(
            keys_by_type=KEYS_BY_TYPE,
            normalizers=NORMALIZERS, **kwds)

        expected = expected and collections.OrderedDict(expected)
        self.assertEqual(md.extract(msg), expected)

    def test_one(self):
        expected = [
            ('channel', 1),
            ('type', 'note_on'),
            ('note', 32),
            ('velocity', fractions.Fraction(96) / 127)]

        self.run_test(C3, expected)
        self.run_test(C3, expected[1:], omit='channel')

    def test_accept(self):
        accept = {'channel': 2, 'type': 'control_change', 'control': 2}
        for msg in C3, C3_OFF, BC3, MOD, OTHER:
            self.run_test(msg, collections.OrderedDict(), accept=accept)

        self.run_test(
            BC,
            [('value', fractions.Fraction(10) / 127)],
            accept=accept)
