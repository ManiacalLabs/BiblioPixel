"""
Run a project description file.
"""

import sys, time, traceback
from . import common_flags, simpixel
from .. util import log
from .. animation.collection import Collection
from .. project import load

RUN_ERROR = """When reading description:
{desc}
encountered exception
{exception}
"""

FAILURE_ERROR = '{count} project{s} failed'


def _get_animations(args):
    animations, failed = [], []

    for project in args.name or ['']:
        saved_path = sys.path[:]
        try:
            desc = load.data(project)
            animations.append(common_flags.make_animation(args, desc))

        except Exception as exception:
            if args.verbose:
                exception = traceback.format_exc()
            failed.append(RUN_ERROR.format(**locals()))

        finally:
            sys.path[:] = saved_path

    if not failed:
        return animations

    log.error(FAILURE_ERROR.format(
        count=len(failed), s='' if len(failed) == 1 else 's'))
    for f in failed:
        log.error(f)
    raise ValueError('Run aborted')


def _run_animations(animations, pause):
    needs_pause = False
    for animation in animations:
        if needs_pause:
            pause and time.sleep(float(pause))
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


def run(args):
    if args.fail_on_exception:
        Collection.FAIL_ON_EXCEPTION = True

    animations = _get_animations(args)

    if args.simpixel:
        simpixel.open_simpixel(args.simpixel)
    elif args.s:
        simpixel.open_simpixel()

    _run_animations(animations, args.pause)


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
