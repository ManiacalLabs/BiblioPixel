import unittest
from bibliopixel.controllers import midi
from argparse import Namespace

C3 = Namespace(type='note_on', note=32, channel=1, velocity=96)
C3_OFF = Namespace(type='note_off', note=32, channel=1, velocity=0, x=47)
BC = Namespace(type='control_change', channel=2, control=2, value=10)
BC3 = Namespace(type='control_change', channel=3, control=2, value=127)
MOD = Namespace(type='control_change', channel=2, control=1, value=127)
PB = Namespace(type='control_change', channel=2, control=1, value=127)
OTHER = Namespace(type='other', channel=32, thing='stuff')


class FakeMido:
    def __init__(self, msgs):
        self.ports = self
        self.ports.MultiPort = lambda x: msgs

    def get_input_names(self):
        return ['one', 'two']

    def open_input(self, x):
        return x


class MidiTest(unittest.TestCase):
    def run_test(self, msgs, expected, **kwds):
        actual = []

        midi.mido, saved_mido = FakeMido(msgs), midi.mido
        try:
            m = midi.Midi(callback=actual.append, **kwds)
            m.start()
            m.thread.join()
            actual = [list(i.items()) for i in actual]
            self.assertEquals(actual, expected)
        finally:
            midi.mido = saved_mido

    def test_one(self):
        expected = [
            ('channel', 1),
            ('type', 'note_on'),
            ('note', 32),
            ('velocity', 96 / 127)]

        self.run_test([C3], [expected])
        self.run_test([C3, C3], [expected, expected])
        self.run_test([C3, C3], [expected[1:], expected[1:]], omit='channel')

    def test_accept(self):
        accept = {'channel': 2, 'type': 'control_change', 'control': 2}
        self.run_test([C3, C3_OFF, BC, BC3, MOD, OTHER],
                      [[('value', 10 / 127)]], accept=accept)
