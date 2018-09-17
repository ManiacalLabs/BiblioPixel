"""
Run a bibliopixel demo
"""

DESCRIPTION = """
For the list of possible demos, type

.. code-block:: bash

    bp demo list

"""

import random

from . import args, common_flags, demo_table
from .. project import project
from .. util import log, pid_context

DEMO_OPTS = ', '.join(sorted(demo_table.DEMO_TABLE.keys()))


def make_runnable_animation(demo, args):
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

    project = common_flags.make_project(args, demo)
    return project.animation


def usage():
    log.printer('Available demos are: {}'.format(DEMO_OPTS))


def run(args):
    if args.name == 'list':
        usage()
        return

    args.simpixel = args.simpixel or True
    if not args.name:
        usage()
        args.name = random.choice(list(demo_table.DEMO_TABLE))
        log.printer('Randomly selected', args.name)

    try:
        demo = demo_table.DEMO_TABLE[args.name]
    except KeyError:
        raise KeyError('Unknown demo %s' % args.name)

    animation = make_runnable_animation(demo, args)
    animation.layout.start()
    animation.start()


def set_parser(parser):
    parser.set_defaults(run=run)
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
