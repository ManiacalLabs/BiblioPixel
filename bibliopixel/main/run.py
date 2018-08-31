"""
Run specified project from file or URL
"""

import os, string, sys, time, traceback
from . import common_flags
from .. util import data_file, log, pid_context, signal_handler
from .. animation import Animation
from .. project import load
from .. project.aliases import ALIAS_MARKERS
from .. project.project import Project

RUN_ERROR = """When reading file {filename}:

{desc}
{exception}
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
    return data_file.dumps(desc, use_yaml=not args.json, safe=False)


def _get_projects(args):
    projects, failed = [], []

    gif = args.gif
    if gif != '':
        log.info('writing animated gifs')
        if gif is None:
            # --get appeared but without a value
            gif = '{}'
        if '{' in gif:
            gif = data_file.loads(gif, filename='--gif')
        if isinstance(gif, str):
            gif = {'filename': gif}
        if 'filename' in gif and len(args.name) > 1:
            log.warning('Writing multiple documents to the same GIF file name')

        gif['typename'] = '.gif_writer'

    # Handle spaces around + signs.
    names = []
    for name in args.name:
        if names and (name.startswith('+') or names[-1].endswith('+')):
            names[-1] += name
        else:
            names.append(name)
    args.name = names

    for project_files in args.name:
        saved_path = sys.path[:]
        descs = []
        try:
            for filename in project_files.split('+'):
                root_file = None
                if filename.endswith('.py'):
                    desc = _load_py(filename)
                elif '{' in filename:
                    desc = data_file.loads(filename)
                else:
                    try:
                        desc = load.data(filename, False)
                        desc = data_file.load(desc, filename)
                        root_file = os.path.abspath(filename)
                    except:
                        if not _might_be_classname(filename):
                            raise
                        desc = {'animation': filename}

                if gif:
                    if 'filename' in gif:
                        desc['driver'] = gif
                    else:
                        f, suffix = os.path.splitext(filename)
                        desc['driver'] = dict(gif, filename=f + '.gif')
                descs.append(desc)

            project = common_flags.make_project(
                args, *descs, root_file=root_file)
            projects.append(project)
            if args.dump:
                log.printer(_dump(args, project.desc))

        except FileNotFoundError as e:
            failed.append(('%s: %s' % (e.strerror, e.filename), ()))

        except Exception as exception:
            if filename.endswith('.py'):
                raise
            eargs = exception.args
            desc = _dump(args, descs)
            if args.verbose:
                exception = traceback.format_exc()
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
    global _RUNNING
    _RUNNING = True

    needs_pause = False
    assert len(projects) == len(args.name)
    is_gif = args.gif != ''

    for project, name in zip(projects, args.name):
        if not _RUNNING:
            break

        if needs_pause:
            if args.pause:
                time.sleep(float(args.pause))
                if not _RUNNING:
                    break
        else:
            needs_pause = True

        log.debug('Running file %s', name)
        if is_gif:
            project.flat_out()

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


def run_once(args):
    Animation.FAIL_ON_EXCEPTION = args.fail_on_exception

    args.name = args.name or ['']
    projects = _get_projects(args)

    if args.dry_run:
        log.printer('(dry run - nothing executed)')
        return

    _run_projects(projects, args)


def stop():
    global _RUNNING
    _RUNNING = False
    Project.stop_all()


def run(args):
    with pid_context.pid_context(args.pid_filename):
        with signal_handler.context(
                SIGHUP=stop, SIGINT=stop, SIGTERM=stop) as signals:
            while True:
                run_once(args)
                if signals:
                    log.info('Received signal %s', ' '.join(signals))

                if not signals.pop('SIGHUP', False):
                    break


def set_parser(parser):
    parser.set_defaults(run=run)
    common_flags.add_project_flags(parser)

    parser.add_argument(
        'name', nargs='*',
        help='Path project files - can be a URL or file system location')


_RUNNING = False
_ALL_CHARS = set(string.ascii_letters + string.digits + '._' + ALIAS_MARKERS)
_START_CHARS = set(string.ascii_letters + '.' + ALIAS_MARKERS)
_END_CHARS = set(string.ascii_letters + string.digits)


def _might_be_classname(s):
    return (s and
            set(s) <= _ALL_CHARS and
            s[0] in _START_CHARS and
            s[-1] in _END_CHARS)
