"""
Run a project description file.
"""

import loady, json, os
from . import common_flags, simpixel
from .. util import log


def run(args):
    common_flags.extend_path(args)
    if args.json:
        desc = args.name
    else:
        desc = args.name and loady.data.load(args.name, True)

    animation = common_flags.make_animation(args, desc or {})

    if args.simpixel:
        simpixel.open_simpixel(args.simpixel)
    elif args.s:
        simpixel.open_simpixel()

    try:
        animation.start()
    except KeyboardInterrupt:
        print('\nTermination requested by user.')
        animation.cleanup()


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.description = 'Run specified BiblioPixel project from file or URL.'

    common_flags.add_project_flags(parser)

    parser.add_argument(
        'name', nargs='?',
        help='Path project file - can be a URL or file system location',
        default='')

    parser.add_argument(
        '-j', '--json', action='store_true',
        help='Enter JSON directly as a command line argument.')
