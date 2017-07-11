"""
Clear the git repository library cache.
"""
import gitty


def run(args, settings):
    gitty.clear_library_cache()


def set_parser(parser):
    parser.set_defaults(run=run)
