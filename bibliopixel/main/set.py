import json, sys
from .. project import merge, defaults


def run(args):
    defaults.set_defaults(args.sections)


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.description = DESCRIPTION
    parser.add_argument('sections', nargs='*')


DESCRIPTION = """
set -- set some or all sections of the project defaults.

Each argument to `bp default set` has to look like

  section=value

Example:

   bp set numbers=float dimensions=80
"""
