import json
from .. project import project
from .. import log
from .. util import files

HELP = """
Run a project description file.
"""


def add_project_default_arguments(parser):
    parser.add_argument(
        '-d', '--driver', default=None,
        help='Default driver type if no driver is specified')

    parser.add_argument(
        '-l', '--layout', default=None,
        help='Default LAYOUT class if no LAYOUT is specified')

    parser.add_argument(
        '-t', '--ledtype', default=None,
        help='Default LED type if no LED type is specified')

    parser.add_argument(
        '-a', '--animation', default=None,
        help='Default animation type if no animation is specified')


def get_project_default_arguments(args):
    return {
        'driver': args.driver,
        'layout': args.layout,
        'animation': args.animation,
        'ledtype': args.ledtype,
    }


def project_to_animation(name, is_json, defaults):
    log.info('Processing project file...')
    data = name if is_json else files.opener(name).read()
    try:
        desc = json.loads(data)
    except ValueError as e:
        e.args += tuple(['in %s' % name])
        raise
    return project.project_to_animation(desc, defaults)


def run(args, settings):
    if args.name:
        defaults = get_project_default_arguments(args)
        project_to_animation(args.name, args.json, defaults).start()


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
