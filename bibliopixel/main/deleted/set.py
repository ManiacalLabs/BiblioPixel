"""
Set some or all sections of the project defaults
"""

DESCRIPTION = """
Each argument to `bp default set` has to look like

section=value

Example:

    bp set numbers=float shape=80

"""

import sys
from ... project import merge, defaults


def run(args):
    defaults.set_defaults(args.sections)


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.add_argument('sections', nargs='*')
