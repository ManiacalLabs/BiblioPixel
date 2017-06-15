from .. project import project
from .. import log

HELP = """
Run a project description file.
"""


def add_project_default_arguments(parser):
    parser.add_argument(
        '-d', '--driver', default=None,
        help='Default driver type if no driver is specified')

    parser.add_argument(
        '-l', '--led', default=None,
        help='Default LED class if no LED is specified')

    parser.add_argument(
        '-t', '--ledtype', default=None,
        help='Default LED type if no LED type is specified')

    parser.add_argument(
        '-a', '--animation', default=None,
        help='Default animation type if no animation is specified')


def get_project_default_arguments(args):
    return {
        'driver': args.driver,
        'led': args.led,
        'animation': args.animation,
        'ledtype': args.ledtype,
    }


def run(args, settings):
    if args.name:
        defaults = get_project_default_arguments(args)
        project.run(args.name, not args.json, defaults)


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

    add_project_default_arguments(parser)
