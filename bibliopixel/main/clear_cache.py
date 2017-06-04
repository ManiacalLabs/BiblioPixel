import gitty

HELP = """
Clear the git repository library cache.
"""


def run(args, settings):
    gitty.clear_library_cache()


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.description = HELP
