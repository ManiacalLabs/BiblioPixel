import random, webbrowser

from . demo_table import DEMO_TABLE
from . import run as _run
from .. project import project

HELP = """
Run a demo.  For the list of possible demos, type

  $ bibliopixel demo list

"""

DEFAULT_SIMPIXEL_URL = 'http://simpixel.io'
DEMO_OPTS = ', '.join(sorted(DEMO_TABLE.keys()))


def make_runnable(demo, args):
    if callable(demo):
        return demo(args).run

    if 'driver' in demo:
        if not demo['driver'].get('num'):
            if 'led' in demo and demo['led']['typename'] == 'cube':
                demo['driver']['num'] = args.width * args.height * args.depth
            else:
                demo['driver']['num'] = args.width * args.height

    if 'led' in demo:
        led = demo['led']
        if 'width' in led:
            led['width'] = led['width'] or args.width
        if 'x' in led:
            led['x'] = led['x'] or args.width
        if 'height' in led:
            led['height'] = led['height'] or args.height
        if 'y' in led:
            led['y'] = led['y'] or args.height
        if 'z' in led:
            led['z'] = led['z'] or args.depth

    defaults = _run.get_project_default_arguments(args)
    return project.project_to_runnable(demo, defaults)


def usage():
    print('Available demos are: {}'.format(DEMO_OPTS))


def run(args, settings):
    if args.name == 'list':
        usage()
        return

    if not args.name:
        usage()
        args.name = random.choice(list(DEMO_TABLE))
        print('Randomly selected', args.name)

    try:
        demo = DEMO_TABLE[args.name]
    except KeyError:
        raise KeyError('Unknown demo %s' % args.name)

    runnable = make_runnable(demo, args)
    if not args.simpixel.startswith('no'):
        webbrowser.open(args.simpixel, new=0, autoraise=True)

    runnable()


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.description = 'Run demo in SimPixel'

    parser.add_argument(
        'name', nargs='?', default='',
        help='Name of demo to run. Options are: {}'.format(DEMO_OPTS))

    parser.add_argument(
        '--width', default=16, type=int,
        help='X dimension of display')

    parser.add_argument(
        '--height', default=16, type=int,
        help='Y dimension of display')

    parser.add_argument(
        '--depth', default=16, type=int,
        help='Z dimension of display. Only used for Cube demos.')

    parser.add_argument(
        '--simpixel', default=DEFAULT_SIMPIXEL_URL,
        help='URL for SimPixel program.')

    _run.add_project_default_arguments(parser)
