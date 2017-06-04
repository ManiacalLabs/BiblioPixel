from .. project import project
from .. import log

HELP = """
Run a project description file.
"""


def run(args, settings):
    if args.name:
        project.run(args.name, not args.json)


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.description = 'Run specified BiblioPixel project from file or URL.'
    parser.add_argument(
        'name', nargs='?',
        help='Path project file - can be a URL or file system location',
        default='')
    parser.add_argument(
        '-j', '--json', action='store_true',
        help='Enter JSON directly as a command line argument.')
