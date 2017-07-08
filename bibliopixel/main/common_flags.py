import json
from .. project import project

"""Common command line arguments for run and demo."""

COMPONENTS = 'driver', 'layout', 'animation'


def add_project_flags(parser):
    parser.add_argument(
        '-d', '--driver', default='simpixel',
        help='Default driver type if no driver is specified')

    parser.add_argument(
        '-l', '--layout', default='matrix',
        help='Default layout class if no layout is specified')

    parser.add_argument(
        '-t', '--ledtype', default=None,
        help='Default LED type if no LED type is specified')

    parser.add_argument(
        '-a', '--animation', default=None,
        help='Default animation type if no animation is specified')

    parser.add_argument(
        '-s', action='store_true', help='Run SimPixel at the default URL')

    parser.add_argument('--simpixel', help='Run SimPixel at a specific URL')


def make_animation(args, desc):
    def get_value(name):
        value = args and getattr(args, name)
        if not value:
            return {}

        if '{' in value:
            return json.loads(value)

        return {'typename': value}

    project_flags = {name: get_value(name) for name in COMPONENTS}
    if args and args.ledtype:
        project_flags['driver']['ledtype'] = args.ledtype

    return project.project_to_animation(desc, project_flags)
