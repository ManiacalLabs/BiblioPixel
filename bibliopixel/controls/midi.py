import functools
from .. import log

try:
    import mido as _mido

    def mido():
        return _mido

except ImportError:
    _mido = None

    def mido():
        raise ImportError('No mido library installed!')


MESSAGE_TYPES = set(
    (s['type'] for s in _mido.messages.specs.SPECS) if _mido else ())

BAD_DEFAULTS = 'IAC Driver Bus',
TYPES_ERROR_FORMAT = 'Bad type "%s". Possible MIDI types are: ' + ', '.join(
    sorted(MESSAGE_TYPES))


def input_names():
    return mido().get_input_names()


def default_input_name():
    names = input_names()

    for name in names:
        for bad in BAD_DEFAULTS:
            if name.startswith(bad):
                break
        else:
            return name

    # There are only bad names, so return the first one.
    return input_names()[0]


def input_name(name=None):
    if name is None:
        return default_input_name()

    names = input_names()
    if name in names:
        return name

    if isinstance(name, int):
        return names[name]

    raise ValueError('Unknown input %s' % name)


def open_one_input(name=None):
    return mido().open_input(input_name(name))


def open_multiport_input(names):
    assert names

    ports = (open_one_input(n) for n in names)
    return mido().ports.MultiPort(ports, yield_ports=True)


def sanitize_midi_message(message):
    """
    The MIDI spec says that note ons with velocity zero are
    note-offs.  We change their type to 'note_off' to make life
    easier for later clients.
    """

    if message.type == 'note_on' and not message.velocity:
        kwds = vars(message)
        kwds['type'] = 'note_off'
        return mido().Message(**kwds)

    return message


def yield_messages(names):
    with open_multiport_input(names) as inport:
        for port, message in inport:
            yield port, sanitize_midi_message(message)


def for_each_message(names, receiver):
    for port, message in yield_messages(names):
        receiver(port, message)


def type_switch(**kwds):
    unknowns = set(kwds) - MESSAGE_TYPES
    if unknowns:
        log.error(TYPES_ERROR_FORMAT, unknowns)

    def receiver(port, message):
        run = kwds.get(message.type)
        run and run(port, message)

    return receiver
