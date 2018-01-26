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
        'aftertouch': (
            'port', 'channel', 'type', 'value'),
        'control_change': (
            'port', 'channel', 'type', 'control', 'value'),
        'note_off': (
            'port', 'channel', 'type', 'note', 'velocity'),
        'note_on': (
            'port', 'channel', 'type', 'note', 'velocity'),
        'pitchwheel': (
            'port', 'channel', 'type', 'pitch'),
        'program_change': (
            'port', 'channel', 'type', 'program'),
    }

    # Some numeric fields (channel, control, program and note) don't get
    # normalized because they are basically names.
    #
    NORMALIZERS = {
        'pitch': lambda x: fractions.Fraction(x - 8192) / 8192,
        'value': lambda x: fractions.Fraction(x) / 127,
        'velocity': lambda x: fractions.Fraction(x) / 127,
    }

    def __init__(self, omit=('port', 'channel'), use_note_off=False, **kwds):
        super().__init__(omit=omit, **kwds)
        self.use_note_off = use_note_off

    def __iter__(self):
        ports = [mido.open_input(i) for i in mido.get_input_names()]

        for port, msg in mido.ports.MultiPort(ports, yield_ports=True):
            mdict = dict(vars(msg), port=port)
            if self.use_note_off or msg.type != 'note_off':
                yield mdict
            else:
                yield dict(mdict, type='note_on', velocity=0)
