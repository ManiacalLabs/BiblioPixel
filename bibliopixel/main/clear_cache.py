import loady

"""
Clear the git repository library cache.
"""


def run(args):
    loady.library.clear()


def set_parser(parser):
    parser.set_defaults(run=run)
