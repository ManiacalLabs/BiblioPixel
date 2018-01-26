import fractions, unittest
from bibliopixel.controllers import midi
from argparse import Namespace
from test.bibliopixel import patch

C3 = Namespace(type='note_on', note=32, channel=1, velocity=96)
C3_OFF = Namespace(type='note_off', note=32, channel=1, velocity=0, x=47)
BC = Namespace(type='control_change', channel=2, control=2, value=10)
BC3 = Namespace(type='control_change', channel=3, control=2, value=127)
MOD = Namespace(type='control_change', channel=2, control=1, value=127)
PB = Namespace(type='control_change', channel=2, control=1, value=127)
OTHER = Namespace(type='other', channel=32, thing='stuff')


class FakeMido:
    def __init__(self, msgs):
        def multi_port(x, yield_ports=False):
            if yield_ports:
                return (('fake_port', i) for i in msgs)
            else:
                return msgs

        self.ports = self
        self.ports.MultiPort = multi_port

    def get_input_names(self):
        return ['one', 'two']

    def open_input(self, x):
        return x


class MidiTest(unittest.TestCase):
    def run_test(self, msgs, expected, **kwds):
        actual = []

        with patch.patch(midi, 'mido', FakeMido(msgs)):
            m = midi.Midi(callback=actual.append, **kwds)
            m.start()
            m.thread.join()
            actual = [list(i.items()) for i in actual]
            if actual != expected:
                print('FAIL')
                print(actual)
                print(expected)
            self.assertEquals(actual, expected)

    def test_one(self):
        expected = [
            ('port', 'fake_port'),
            ('channel', 1),
            ('type', 'note_on'),
            ('note', 32),
            ('velocity', fractions.Fraction(96) / 127)]

        self.run_test([C3], [expected[2:]])
        self.run_test([C3, C3], [expected[2:], expected[2:]])
        self.run_test([C3], [expected], omit=None)

    def test_accept(self):
        accept = {'channel': 2, 'type': 'control_change', 'control': 2}
        expected = [('value', fractions.Fraction(10) / 127)]
        self.run_test(
            [C3, C3_OFF, BC, BC3, MOD, OTHER], [expected], accept=accept)
