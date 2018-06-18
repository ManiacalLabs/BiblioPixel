import fractions
from . import control
from .. util import log

try:
    import mido
    MESSAGE_TYPES = set(s['type'] for s in mido.messages.specs.SPECS)

except:
    mido = None
    MESSAGE_TYPES = set()

MIDO_ERROR = """You need to install mido.  Try
    pip install mido
"""

MIDO_BACKEND_ERROR = """You have the wrong rtmidi installed.  Try
    pip uninstall -y rtmidi
    pip install -y python-rtmidi
"""


class Midi(control.ExtractedLoop):
    EXTRACTOR = {
        # There are more mido message types that we haven't used yet.
        'keys_by_type': {
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
        },

        # Some numeric fields (channel, control, program and note) don't get
        # normalized because they are basically names.
        'normalizers': {
            'pitch': lambda x: fractions.Fraction(x - 8192) / 8192,
            'value': lambda x: fractions.Fraction(x) / 127,
            'velocity': lambda x: fractions.Fraction(x) / 127,
        },

        'omit': ('port', 'channel'),
    }

    def __init__(self, use_note_off=True, **kwds):
        """
        :param use_note_off:
            If False, map note_offs to note_ons with velocity 0
            If True, map note_ons with velocity 0 to note_offs
            If None, do not change none_ons or note_offs
        """
        control.ExtractedControl.__init__(self, **kwds)
        self.use_note_off = use_note_off

    def messages(self):
        if not mido:
            raise ValueError(MIDO_ERROR)
        try:
            input_names = mido.get_input_names()
        except AttributeError as e:
            e.args = (MIDO_ERROR,) + e.args
            raise

        ports = [mido.open_input(i) for i in input_names]

        if not ports:
            log.error('control.midi: no MIDI ports found')
            return

        port_names = ', '.join('"%s"' % p.name for p in ports)
        log.info('Starting to listen for MIDI on port%s %s',
                 '' if len(ports) == 1 else 's', port_names)
        for port, msg in mido.ports.MultiPort(ports, yield_ports=True):
            mdict = dict(vars(msg), port=port)

            if self.use_note_off:
                if msg.type == 'note_on' and not msg.velocity:
                    mdict.update(type='note_off')
            elif self.use_note_off is False:
                if msg.type == 'note_off':
                    mdict.update(type='note_on', velocity=0)

            yield mdict
