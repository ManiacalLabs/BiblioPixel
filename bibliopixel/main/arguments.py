import json
from .. project import project

"""Common command line arguments for run and demo."""

COMPONENTS = 'driver', 'layout', 'animation'


def add_to_parser(parser):
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


def get_dict(args):
    def get_value(name):
        value = args and getattr(args, name)
        if not value:
            return {}

        if '{' in value:
            return json.loads(value)

        return {'typename': value}

    result = {name: get_value(name) for name in COMPONENTS}
    if args and args.ledtype:
        result['driver']['ledtype'] = args.ledtype

    return result


def make_animation(args, desc):
    return project.project_to_animation(desc, get_dict(args))
