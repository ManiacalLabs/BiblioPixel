import argparse, os, sys
from . import commands, common_flags
from .. util import log
from .. project import aliases, project

__all__ = ['main']


def get_args(argv=sys.argv):
    argv = ['-h' if a == '--help' else a for a in argv[1:]]

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
        subparser.description = doc + commands.un_md(description)

    if argv == ['-h']:
        log.printer(commands.HELP)

    return parser.parse_args(argv)


def main():
    args = get_args()
    run = getattr(args, 'run', None)
    if not run:
        log.printer('ERROR: No command entered')
        log.printer('Valid commands are:')
        log.printer('    ', ', '.join(commands.COMMANDS))
        log.printer()
        log.printer('For more help, type')
        log.printer()
        log.printer('    bp --help')
        sys.exit(-1)

    common_flags.execute_args(args)

    try:
        return run(args) or 0
    except Exception as e:
        if args.verbose:
            raise
        log.printer('ERROR:', e.args[0], file=sys.stderr)
        log.printer(*e.args[1:], sep='\n', file=sys.stderr)
        result = getattr(e, 'errorcode', -1)

    sys.exit(result)
