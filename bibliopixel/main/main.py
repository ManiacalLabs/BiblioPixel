import argparse, gitty, os, sys
from .. import log
from .. project.importer import import_symbol
from .. project.preset_library import PresetLibrary

__all__ = ['main']

COMMANDS = ('all_pixel', 'clear_cache', 'color', 'devices', 'demo', 'run')

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

VERBOSE_HELP = """\
If this is set, then errors are reported with a full stack trace.
If not set, just the exception message is printed.
"""


def _get_version():
    from os.path import abspath, dirname, join
    filename = join(dirname(dirname(dirname(abspath(
        __file__)))), 'bibliopixel', 'VERSION')
    return open(filename).read().strip()


VERSION = _get_version()
VERSION_HELP = """\
Print the current version number of BiblioPixel (%s).
""" % VERSION


def no_command(*_):
    print('ERROR: No command entered')
    print('Valid:', ', '.join(COMMANDS))
    return -1


def main():
    parser = argparse.ArgumentParser()
    flags = set()

    def add(*args, **kwds):
        flags.update(args)
        parser.add_argument(*args, **kwds)

    subparsers = parser.add_subparsers()

    for name, module in sorted(MODULES.items()):
        subparser = subparsers.add_parser(name, help=module.HELP)
        module.set_parser(subparser)

    add('--loglevel', choices=LOG_LEVELS, default='info', help=LOGLEVEL_HELP)
    add('--path', default=None, help=PATH_HELP)
    add('--verbose', '-v', action='store_true', help=VERBOSE_HELP)
    add('--version', action='store_true', help=VERSION_HELP)

    if ENABLE_PRESETS:
        add('--presets', help='Filename for presets',
            default=PRESET_LIBRARY_DEFAULT)

    argv = ['--help' if i == 'help' else i for i in sys.argv[1:]]

    try:
        argv.remove('--version')
    except:
        pass
    else:
        print('BiblioPixel version %s' % VERSION)
        if not argv:
            return

    # Move global flags to the start.
    ok, removed = [], []

    for a in argv:
        (removed if a.split('=')[0] in flags else ok).append(a)

    args = parser.parse_args(removed + ok)

    try:
        log.set_log_level(args.loglevel)
        presets = ENABLE_PRESETS and PresetLibrary(
            os.path.expanduser(args.presets), True)

        run = getattr(args, 'run', no_command)
        gitty.sys_path.extend(args.path)
        result = run(args, presets) or 0

    except Exception as e:
        if args.verbose:
            raise
        print('ERROR:', e.args[0], file=sys.stderr)
        print(*e.args[1:], sep='\n', file=sys.stderr)
        result = getattr(e, 'errorcode', -1)

    sys.exit(result)
