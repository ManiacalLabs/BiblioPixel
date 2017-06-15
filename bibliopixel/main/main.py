import argparse, gitty, os, sys
from .. import log
from .. project.importer import import_symbol
from .. project.preset_library import PresetLibrary

__all__ = ['main']

COMMANDS = ('all_pixel', 'clear_cache', 'devices', 'demo', 'run')
MODULES = {c: import_symbol('.' + c, 'bibliopixel.main') for c in COMMANDS}
PRESET_LIBRARY_DEFAULT = '~/.bibliopixel'
LOG_LEVELS = ('debug', 'info', 'warning', 'error', 'critical')
ENABLE_PRESETS = False

PATH_HELP = """\
A list of directories, separated by colons, 'which are added to the end of
`sys.path`.

You can also use gitty-style paths which start with `//git/` to
dynamically load a library from a public git repository.

See https://github.com/ManiacalLabs/BiblioPixel/wiki/BiblioPixel-Paths
for more information.
"""

LOGLEVEL_HELP = """\
Set what level of events to log. Higher log levels print less."""


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
    parser.add_argument('--loglevel', choices=LOG_LEVELS, default='info',
                        help=LOGLEVEL_HELP)
    parser.add_argument('--path', default=None,
                        help=PATH_HELP)
    if ENABLE_PRESETS:
        parser.add_argument('--presets', help='Filename for presets',
                            default=PRESET_LIBRARY_DEFAULT)

    args = ['--help' if i == 'help' else i for i in sys.argv[1:]]
    args = parser.parse_args(args)

    log.set_log_level(args.loglevel)
    presets = ENABLE_PRESETS and PresetLibrary(
        os.path.expanduser(args.presets), True)

    run = getattr(args, 'run', no_command)
    gitty.sys_path.extend(args.path)
    sys.exit(run(args, presets) or 0)
