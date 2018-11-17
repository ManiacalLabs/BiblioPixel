"""
Clear the loady git repository library cache
"""

import loady


def run(args):
    loady.library.clear()


def add_arguments(parser):
    parser.set_defaults(run=run)
