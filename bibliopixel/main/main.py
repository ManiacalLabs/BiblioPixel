import argparse, os, sys
from .. import log
from .. project.importer import import_symbol
from .. project.preset_library import PresetLibrary

__all__ = ['main']

COMMANDS = ('all_pixel', 'devices', 'demo', 'run', 'set', 'show')
MODULES = {c: import_symbol('.' + c, 'bibliopixel.main') for c in COMMANDS}
PRESET_LIBRARY_DEFAULT = '~/.bibliopixel'
LOG_LEVELS = ('debug', 'info', 'warning', 'error', 'critical')


def no_command(*_):
    print('ERROR: No command entered')
    print('Valid:', *COMMANDS)
    return -1


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    for name, module in sorted(MODULES.items()):
        subparser = subparsers.add_parser(name, help=module.HELP)
        module.set_parser(subparser)
    parser.add_argument('--loglevel', choices=LOG_LEVELS, default='info')
    parser.add_argument('--settings',
                        help='Filename for settings',
                        default=PRESET_LIBRARY_DEFAULT)

    args = ['--help' if i == 'help' else i for i in sys.argv[1:]]
    args = parser.parse_args(args)

    log.set_log_level(args.loglevel)
    settings = PresetLibrary(os.path.expanduser(args.settings), True)

    run = getattr(args, 'run', no_command)
    sys.exit(run(args, settings) or 0)
