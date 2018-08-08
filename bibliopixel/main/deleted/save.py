"""
Save the current project defaults to a file
"""

from ... project import defaults


def run(args):
    defaults.save_defaults(args.name)


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.add_argument('name', help='Save the current defaults setting')
