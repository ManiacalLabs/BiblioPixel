import argparse, os, sys
from .. util.importer import import_symbol
from .. project.settings_file import SettingsFile

__all__ = ['main']

COMMANDS = ('demo', 'run', 'set', 'show',)  # 'network'
MODULES = {c: import_symbol('.' + c, 'bibliopixel.main') for c in COMMANDS}
DOTFILE_DEFAULT = '~/.bibliopixel'


def no_command(*_):
    print('ERROR: No command entered')
    print('Valid:', *COMMANDS)
    return -1


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    for name, module in MODULES.items():
        subparser = subparsers.add_parser(name, help=module.HELP)
        module.set_parser(subparser)
    parser.add_argument('--settings',
                        help='Filename for settings', default=DOTFILE_DEFAULT)

    args = parser.parse_args()
    settings = SettingsFile(os.path.expanduser(args.settings), True)
    run = getattr(args, 'run', no_command)
    sys.exit(run(args, settings) or 0)
