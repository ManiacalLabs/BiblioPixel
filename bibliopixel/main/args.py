import argparse, sys
from .. util import log

ARGS = None


def parse_args(commands, common_flags):
    helps = '--help', 'help'
    argv = ['-h' if a in helps else a for a in sys.argv[1:]]

    if not argv:
        argv = ['-h']

    # argparse doesn't give command-specific help for `bp --help <command>`
    # so we use `bp <command> --help` (#429)
    if len(argv) == 2 and argv[0] == '-h':
        argv.reverse()

    try:
        argv.remove('--version')
    except:
        pass
    else:
        log.printer('BiblioPixel version %s' % common_flags.VERSION)
        if not argv:
            return

    # Move all the flags to the end.
    args = [], []
    for a in argv:
        args[a.startswith('-')].append(a)

    argv = args[0] + args[1]

    if not argv[0].isidentifier() and '-h' not in argv:
        # The first argument can't be a command so try to run it.
        argv.insert(0, 'run')

    if argv and argv[0].startswith('-') and any(
            not a.startswith('-') for a in argv):
        log.printer(
            'bibliopixel: error: command line flags must appear at the end.')

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    for name, module in sorted(commands.MODULES.items()):
        doc = module.__doc__
        subparser = subparsers.add_parser(name, help=doc)
        common_flags.add_common_flags(subparser)
        module.set_parser(subparser)
        description = getattr(module, 'DESCRIPTION', '')
        subparser.description = doc + description

    if argv == ['-h']:
        log.printer(commands.HELP)

    global ARGS
    ARGS = parser.parse_args(argv)
