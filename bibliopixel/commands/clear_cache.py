"""
Clear the loady git repository library cache
"""

import loady


def run(args):
    loady.library.clear()


def set_parser(parser):
    parser.set_defaults(run=run)
