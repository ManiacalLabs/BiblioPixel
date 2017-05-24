from bibliopixel.project import paths

HELP = """
Clear the git repository library cache.
"""


def run(args, settings):
    paths.clear_cache()


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.description = HELP
