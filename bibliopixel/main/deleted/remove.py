"""
Remove a project default file
"""
from ... project import defaults


def run(args):
    defaults.remove_defaults(args.name)


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.add_argument('name', help='Remove a saved project defaults')
