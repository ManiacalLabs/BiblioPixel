from .. import log
import functools

MISSING_NOTE_ON_ERROR = 'Note off {0.note}:{0.channel} without note on'


def counter_callbacks(note_on, note_off=None):
    """
    Count the notes that are being held down into a dictionary.

    A note is represented by a triple:
        (port.name, message.channel, message.note)

    The note_counter dictionary maps notes to positive integer counts.

    Arguments:
        note_on, note_off: these are callback functions which expect to get
            two parameters: note, note_counter.

    """
    note_counter = {}
    note_off = note_off or note_on

    @functools.wraps(note_on)
    def on(port, message):
        note = port.name, message.channel, message.note
        count = note_counter.get(note, 0)
        note_counter[note] = 1 + count
        note_on(note, note_counter)

    @functools.wraps(note_off)
    def off(port, message):
        note = port.name, message.channel, message.note
        count = note_counter.get(note, 0)

        if count > 1:
            note_counter[note] = count - 1
        elif count == 1:
            del note_counter[note]
        else:
            log.error(MISSING_NOTE_ON_ERROR.format(message))

        note_off(note, note_counter)

    return {'note_on': on, 'note_off': off}
