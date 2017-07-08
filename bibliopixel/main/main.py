import argparse, gitty, os, sys
from . import common_flags
from .. import log
from .. project.importer import import_symbol
from .. project.preset_library import PresetLibrary

__all__ = ['main']
COMMANDS = (
    'all_pixel', 'clear_cache', 'color', 'devices', 'demo', 'run', 'update')
MODULES = {c: import_symbol('.' + c, 'bibliopixel.main') for c in COMMANDS}


def no_command(*_):
    print('ERROR: No command entered')
    print('Valid:', ', '.join(COMMANDS))
    return -1


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    for name, module in sorted(MODULES.items()):
        subparser = subparsers.add_parser(name, help=module.__doc__)
        module.set_parser(subparser)

    common_flags.add_common_flags(parser)

    argv = ['--help' if i == 'help' else i for i in sys.argv[1:]]

    try:
        argv.remove('--version')
    except:
        pass
    else:
        print('BiblioPixel version %s' % common_flags.VERSION)
        if not argv:
            return
    args = parser.parse_args(argv)

    try:
        log.set_log_level(args.loglevel)
        presets = common_flags.ENABLE_PRESETS and PresetLibrary(
            os.path.expanduser(args.presets), True)

        run = getattr(args, 'run', no_command)
        result = run(args, presets) or 0
    except Exception as e:
        if args.verbose:
            raise
        print('ERROR:', e.args[0], file=sys.stderr)
        print(*e.args[1:], sep='\n', file=sys.stderr)
        result = getattr(e, 'errorcode', -1)

    sys.exit(result)
