"""Monitors MIDI messages."""

from .. controls import count_notes, midi


def run(args, settings):
    names = args.names or midi.input_names()
    switch = midi.type_switch(**count_notes.counter_callbacks(print))

    midi.for_each_message(names, switch)


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.add_argument(
        'names', nargs='*',
        help='Names of MIDI input ports to monitor - default is all of them.')
