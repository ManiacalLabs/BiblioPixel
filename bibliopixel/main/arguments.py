"""Common command line arguments for run and demo."""


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
    result = {}
    for name in 'driver', 'layout', 'animation':
        value = getattr(args, name)
        if value:
            result[name] = value

    if args.ledtype:
        result.setdefault('driver', {})['ledtype'] = args.ledtype

    return result
