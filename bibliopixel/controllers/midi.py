import fractions
from . import control_source

try:
    import mido
    MESSAGE_TYPES = set(s['type'] for s in mido.messages.specs.SPECS)

except:
    mido = None
    MESSAGE_TYPES = set()


class Midi(control_source.ExtractedSource):
    """
    Midi is an ExtractorControlSource for MIDI messages.

    The input description is either a list of MIDI port names, or None, in
    which case all MIDI data from all MIDI ports is used.
    """

    # KEYS_BY_TYPE is a dictionary by message type of the fields we extract from
    # mido MIDI messages.
    # There are more mido message types that we haven't used yet.
    KEYS_BY_TYPE = {
        'aftertouch': ('channel', 'type', 'value'),
        'control_change': ('channel', 'type', 'control', 'value'),
        'note_off': ('channel', 'type', 'note', 'velocity'),
        'note_on': ('channel', 'type', 'note', 'velocity'),
        'pitchwheel': ('channel', 'type', 'pitch'),
        'program_change': ('channel', 'type', 'program'),
    }

    # Some numeric fields (channel, control, program and note) don't get
    # normalized because they are basically names.
    #
    NORMALIZERS = {
        'pitch': lambda x: fractions.Fraction(x - 8192) / 8192,
        'value': lambda x: fractions.Fraction(x) / 127,
        'velocity': lambda x: fractions.Fraction(x) / 127,
    }

    def __iter__(self):
        inputs = mido.get_input_names()
        for msg in mido.ports.MultiPort(mido.open_input(i) for i in inputs):
            yield vars(msg)
