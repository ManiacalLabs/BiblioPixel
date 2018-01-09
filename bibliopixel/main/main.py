import argparse, os, sys
from . import common_flags
from .. util import log
from .. project.importer import import_module
from .. project import aliases, project


__all__ = ['main']
COMMANDS = (
    'all_pixel', 'all_pixel_test', 'clear_cache', 'color', 'demo',
    'devices', 'info', 'load', 'list', 'remove', 'reset', 'run', 'save', 'set',
    'show', 'update')
MODULES = {c: import_module('bibliopixel.main.' + c) for c in COMMANDS}


def no_command(*_):
    log.printer('ERROR: No command entered')
    log.printer('Valid:', ', '.join(COMMANDS))
    return -1


def get_args(argv=sys.argv):
    argv = argv[1:]

    # argparse doesn't give command-specific help for `bp --help <command>`
    # so we use `bp <command> --help` (#429)
    if len(argv) == 2 and argv[0] == '--help':
        argv.reverse()

    try:
        argv.remove('--version')
    except:
        pass
    else:
        log.printer('BiblioPixel version %s' % common_flags.VERSION)
        if not argv:
            return

    if argv and not argv[0].isidentifier() and '--help' not in argv:
        # The first argument can't be a command so try to run it.
        argv.insert(0, 'run')

    if argv and argv[0].startswith('-') and any(
            not a.startswith('-') for a in argv):
        log.printer(
            'bibliopixel: error: command line flags must appear at the end.')

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    for name, module in sorted(MODULES.items()):
        doc = module.__doc__
        subparser = subparsers.add_parser(name, help=doc)
        common_flags.add_common_flags(subparser)
        module.set_parser(subparser)
        subparser.description = doc + getattr(module, 'DESCRIPTION', '')

    return parser.parse_args(argv)


def main():
    args = get_args()
    run = getattr(args, 'run', None)
    if not run:
        log.printer('ERROR: No command entered')
        log.printer('Valid commands are:')
        log.printer('    ', ', '.join(COMMANDS))
        log.printer()
        log.printer('For more help, type')
        log.printer()
        log.printer('    bp --help')
        sys.exit(-1)

    if args.verbose and args.loglevel != 'frame':
        log.set_log_level('debug')
    else:
        log.set_log_level(args.loglevel)

    try:
        return run(args) or 0
    except Exception as e:
        if args.verbose:
            raise
        log.printer('ERROR:', e.args[0], file=sys.stderr)
        log.printer(*e.args[1:], sep='\n', file=sys.stderr)
        result = getattr(e, 'errorcode', -1)

    sys.exit(result)
