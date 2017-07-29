"""
Run a demo.  For the list of possible demos, type

  $ bibliopixel demo list

"""

import random

from . import common_flags, demo_table, simpixel
from .. project import project

DEMO_OPTS = ', '.join(sorted(demo_table.DEMO_TABLE.keys()))


def make_runnable(demo, args):
    if callable(demo):
        return demo(args).run

    if 'driver' in demo:
        if not demo['driver'].get('num'):
            if 'layout' in demo and demo['layout']['typename'] == 'cube':
                demo['driver']['num'] = args.width * args.height * args.depth
            else:
                demo['driver']['num'] = args.width * args.height

    if 'layout' in demo:
        layout = demo['layout']
        if 'width' in layout:
            layout['width'] = layout['width'] or args.width
        if 'x' in layout:
            layout['x'] = layout['x'] or args.width
        if 'height' in layout:
            layout['height'] = layout['height'] or args.height
        if 'y' in layout:
            layout['y'] = layout['y'] or args.height
        if 'z' in layout:
            layout['z'] = layout['z'] or args.depth

    return common_flags.make_animation(args, demo).start


def usage():
    print('Available demos are: {}'.format(DEMO_OPTS))


def run(args):
    if args.name == 'list':
        usage()
        return

    common_flags.extend_path(args)

    if not args.name:
        usage()
        args.name = random.choice(list(demo_table.DEMO_TABLE))
        print('Randomly selected', args.name)

    try:
        demo = demo_table.DEMO_TABLE[args.name]
    except KeyError:
        raise KeyError('Unknown demo %s' % args.name)

    runnable = make_runnable(demo, args)
    simpixel.open_simpixel(args.simpixel)
    runnable()


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.description = 'Run demo in SimPixel'

    common_flags.add_project_flags(parser)
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
