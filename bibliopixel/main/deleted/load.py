"""
Load a saved project default file
"""

from ... project import defaults


def run(args):
    defaults.load_defaults(args.name)


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.add_argument('name', help='Load a defaults setting')
