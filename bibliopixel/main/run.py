"""
Run specified project from file or URL.
"""

import os, sys, time, traceback
from . import common_flags, simpixel
from .. util import json, log
from .. animation import Animation
from .. project import load

RUN_ERROR = """When reading file {filename}:
{desc}
"""

FAILURE_ERROR = """\
{count} project{s} failed
____________________
"""


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


def _dump(args, desc):
    if not isinstance(desc, str):
        desc = json.yaml.dump(desc) if args.yaml else json.dumps(desc)
    return desc.strip()


def _get_projects(args):
    projects, failed = [], []

    for filename in args.name:
        saved_path = sys.path[:]
        desc = '(not loaded)'
        try:
            if filename.endswith('.py'):
                desc = _load_py(filename)
                root_file = None
            else:
                desc = load.data(filename, False)
                desc = json.loads(desc, filename)
                root_file = os.path.abspath(filename)

            project = common_flags.make_project(args, desc, root_file)
            projects.append(project)
            if args.dump:
                print(_dump(args, project.desc))

        except FileNotFoundError as e:
            failed.append(('%s: %s' % (e.strerror, e.filename), ()))

        except Exception as exception:
            if args.verbose or filename.endswith('.py'):
                raise
            eargs = exception.args
            if args.verbose:
                exception = traceback.format_exc()
            desc = desc and _dump(args, desc)
            msg = RUN_ERROR.format(**locals())
            failed.append((msg, eargs))

        finally:
            sys.path[:] = saved_path

    if not failed:
        return projects

    log.error(FAILURE_ERROR.format(
        count=len(failed), s='' if len(failed) == 1 else 's'))
    for msg, args in failed:
        if args:
            log.error(msg + '\n' + '\n'.join(str(a) for a in args) + '\n')
        else:
            log.error(msg + '\n')
    raise ValueError('Run aborted')


def _run_projects(projects, args):
    needs_pause = False
    assert len(projects) == len(args.name)
    for project, name in zip(projects, args.name):
        log.debug('Running file %s', name)
        if needs_pause:
            args.pause and time.sleep(float(args.pause))
        else:
            needs_pause = True

        try:
            project.run()

        except KeyboardInterrupt:
            if not args.ignore_exceptions:
                raise
            log.warning('\nKeyboardInterrupt terminated project.')
            needs_pause = False

        except Exception as e:
            if not args.ignore_exceptions:
                raise
            log.error('Exception %s', e)
            traceback.print_exc()


def run(args):
    Animation.FAIL_ON_EXCEPTION = args.fail_on_exception

    args.name = args.name or ['']
    projects = _get_projects(args)

    if args.dry_run:
        print('(dry run - nothing executed)')
        return
    if args.simpixel:
        simpixel.open_simpixel(args.simpixel)
    elif args.s:
        simpixel.open_simpixel()

    _run_projects(projects, args)


def set_parser(parser):
    parser.set_defaults(run=run)
    common_flags.add_project_flags(parser)

    parser.add_argument(
        'name', nargs='*',
        help='Path project files - can be a URL or file system location')

    parser.add_argument(
        '-j', '--json', action='store_true',
        help='Enter JSON directly as a command line argument.')
