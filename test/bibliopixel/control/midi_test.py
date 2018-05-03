import fractions, time, unittest
from bibliopixel.control import midi
from argparse import Namespace
from test.bibliopixel import patch

C3 = Namespace(type='note_on', note=32, channel=1, velocity=96)
C3_OFF = Namespace(type='note_off', note=32, channel=1, velocity=0, x=47)
BC = Namespace(type='control_change', channel=2, control=2, value=10)
BC3 = Namespace(type='control_change', channel=3, control=2, value=127)
MOD = Namespace(type='control_change', channel=2, control=1, value=127)
PB = Namespace(type='pitchwheel', channel=2, pitch=0x400)
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
        class Port(str):
            def name(self):
                return self

        return [Port('one'), Port('two')]

    def open_input(self, x):
        return x


class MidiTest(unittest.TestCase):
    routing = {
        'note_on': '.note',
        'control_change': {
            '1': '.cc1',
            '2': '.cc2',
        },
        'pitchwheel': '.pitch',
    }

    def run_test(self, msgs, expected, routing=None, **kwds):
        with patch.patch(midi, 'mido', FakeMido(msgs)):
            class Root:
                pass

            root = Root()
            m = midi.Midi(routing=routing or self.routing, **kwds)
            m.set_root(root)
            with m.joiner(stop=True):
                time.sleep(0.1)

            self.assertEqual(vars(root), expected)

    def test_one(self):
        expected = {'note': (32, fractions.Fraction(96, 127))}
        self.run_test([C3], expected)

    def test_accept(self):
        expected = {
            'cc1': 1,
            'cc2': 1,
            'note': (32, 0),
            'pitch': fractions.Fraction(-7, 8),
        }
        self.run_test([C3, C3_OFF, BC, BC3, MOD, PB, OTHER], expected)
