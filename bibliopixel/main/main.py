import argparse, os, sys
from . import common_flags
from .. util import log
from .. project.importer import import_symbol
from .. project import aliases


__all__ = ['main']
COMMANDS = (
    'alias', 'all_pixel', 'clear_cache', 'color', 'devices', 'demo', 'run',
    'update')
MODULES = {c: import_symbol('bibliopixel.main.' + c) for c in COMMANDS}


def no_command(*_):
    print('ERROR: No command entered')
    print('Valid:', ', '.join(COMMANDS))
    return -1


def get_args(argv=sys.argv):
    argv = ['--help' if i == 'help' else i for i in argv[1:]]
    try:
        argv.remove('--version')
    except:
        pass
    else:
        print('BiblioPixel version %s' % common_flags.VERSION)
        if not argv:
            return

    if argv and not argv[0].isidentifier():
        # The first argument can't be a command so try to run it.
        argv.insert(0, 'run')

    if argv and argv[0].startswith('-'):
        print('bibliopixel: error: command line flags must appear at the end.')

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    for name, module in sorted(MODULES.items()):
        subparser = subparsers.add_parser(name, help=module.__doc__)
        common_flags.add_common_flags(subparser)
        module.set_parser(subparser)

    return parser.parse_args(argv)


def main():
    args = get_args()
    run = getattr(args, 'run', None)
    if not run:
        print('ERROR: No command entered')
        print('Valid:', ', '.join(COMMANDS))
        sys.exit(-1)

    aliases.ISOLATE = args.isolate
    log.set_log_level(args.loglevel)

    try:
        return run(args) or 0
    except Exception as e:
        if args.verbose:
            raise
        print('ERROR:', e.args[0], file=sys.stderr)
        print(*e.args[1:], sep='\n', file=sys.stderr)
        result = getattr(e, 'errorcode', -1)

    sys.exit(result)
