"""
Run a project description file.
"""

import os, sys, time, traceback
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


def _load_py(filename):
    module = load.module(filename)
    project = module.get('PROJECT', {})

    if 'animation' not in project:
        no_extension = os.path.splitext(filename)[0]
        module_name = os.path.split(no_extension)[-1]
        names = module.keys()
        try:
            animation_name = load.guess_name(names, module_name, filename)
        except:
            if 'Animation' not in names:
                raise ValueError('Cannot deduce animation in file ' + filename)
            animation_name = 'Animation'
        animation = module[animation_name]
        if not callable(animation):
            raise ValueError('Animation "%s" in file "%s" is not callable'
                             % (animation_name, filename))

        project['animation'] = {'datatype': animation}

    return project


def _get_animations(args):
    animations, failed = [], []

    for filename in args.name:
        saved_path = sys.path[:]
        desc = '(not loaded)'
        try:
            if filename.endswith('.py'):
                desc = _load_py(filename)
            else:
                desc = load.data(filename)
            animation = common_flags.make_animation(args, desc)
            animations.append(animation)

        except Exception as exception:
            if filename.endswith('.py'):
                raise
            if args.verbose:
                exception = traceback.format_exc()
            msg = RUN_ERROR.format(**locals())
            failed.append((msg, exception.args))

        finally:
            sys.path[:] = saved_path

    if not failed:
        return animations

    log.error(FAILURE_ERROR.format(
        count=len(failed), s='' if len(failed) == 1 else 's'))
    for msg, args in failed:
        log.error(msg + '\n' + '\n'.join(str(a) for a in args))
    raise ValueError('Run aborted')


def _run_animations(animations, pause, names):
    needs_pause = False
    assert len(animations) == len(names)
    for animation, name in zip(animations, names):
        log.debug('Running file %s', name)
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

    args.name = args.name or ['']
    animations = _get_animations(args)

    if args.simpixel:
        simpixel.open_simpixel(args.simpixel)
    elif args.s:
        simpixel.open_simpixel()

    _run_animations(animations, args.pause, args.name)


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
