import argparse, os, sys
from .. import log
from .. project.importer import import_symbol
from .. project import paths
from .. project.preset_library import PresetLibrary

__all__ = ['main']

COMMANDS = ('all_pixel', 'devices', 'demo', 'run')  # 'set', 'show')
MODULES = {c: import_symbol('.' + c, 'bibliopixel.main') for c in COMMANDS}
PRESET_LIBRARY_DEFAULT = '~/.bibliopixel'
LOG_LEVELS = ('debug', 'info', 'warning', 'error', 'critical')
ENABLE_PRESETS = False


def no_command(*_):
    print('ERROR: No command entered')
    print('Valid:', ', '.join(COMMANDS))
    return -1


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    for name, module in sorted(MODULES.items()):
        subparser = subparsers.add_parser(name, help=module.HELP)
        module.set_parser(subparser)
    parser.add_argument('--loglevel', choices=LOG_LEVELS, default='info')
    parser.add_argument('--path', default=None,
                        help='A list of directories, separated by colons, '
                        'which are added to the end of `sys.path`')
    if ENABLE_PRESETS:
        parser.add_argument('--presets',
                            help='Filename for presets',
                            default=PRESET_LIBRARY_DEFAULT)

    args = ['--help' if i == 'help' else i for i in sys.argv[1:]]
    args = parser.parse_args(args)

    log.set_log_level(args.loglevel)
    presets = ENABLE_PRESETS and PresetLibrary(
        os.path.expanduser(args.presets), True)

    run = getattr(args, 'run', no_command)
    paths.extend_sys_path(args.path)
    sys.exit(run(args, presets) or 0)
