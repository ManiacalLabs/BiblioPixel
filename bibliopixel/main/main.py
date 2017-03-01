import argparse, sys
from .. util.importer import import_symbol

__all__ = ['main']

COMMANDS = 'demo',  # 'device', 'network', 'run', 'settings'
MODULES = {c: import_symbol('.' + c, 'bibliopixel.main') for c in COMMANDS}


def no_command(_):
    print('ERROR: No command entered')
    print('Valid:', *COMMANDS)
    return -1


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    for name, module in MODULES.items():
        subparser = subparsers.add_parser(name)
        module.set_parser(subparser)

    args = parser.parse_args()
    run = getattr(args, 'run', no_command)
    sys.exit(run(args) or 0)
