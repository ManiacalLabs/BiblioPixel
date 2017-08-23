"""
Run a project description file.
"""

import loady, json, os, time
from . import common_flags, simpixel
from .. util import log

RUN_ERROR = """When reading description:
{desc}
encounted exception
{exception}
"""

FAILURE_ERROR = '{count} project{s} failed'


def run(args):
    common_flags.extend_path(args)

    animations, failed = [], []

    for name in args.name or ['']:
        if args.json:
            desc = name
        else:
            desc = name and loady.data.load(name, True)

        try:
            animations.append(common_flags.make_animation(args, desc or {}))
        except Exception as exception:
            failed.append(RUN_ERROR.format(**locals()))

    if failed:
        log.error(FAILURE_ERROR.format(
            count=len(failed), s='' if len(failed) == 1 else 's'))
        for f in failed:
            log.error(f)
        raise ValueError('Run aborted')

    if args.simpixel:
        simpixel.open_simpixel(args.simpixel)
    elif args.s:
        simpixel.open_simpixel()

    needs_pause = False
    for animation in animations:
        if needs_pause:
            args.pause and time.sleep(float(args.pause))
        else:
            needs_pause = True

        try:
            animation.layout.start()
            animation.start()
        except KeyboardInterrupt:
            log.warning('\nTermination requested by user.')
            needs_pause = False

        animation.cleanup()
        animation.layout.cleanup_drivers()


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.description = 'Run specified BiblioPixel project from file or URL.'

    common_flags.add_project_flags(parser)

    parser.add_argument(
        'name', nargs='*',
        help='Path project files - can be a URL or file system location')

    parser.add_argument(
        '-j', '--json', action='store_true',
        help='Enter JSON directly as a command line argument.')
