"""
Run specified project from file or URL
"""

import os, string, sys, time, traceback
from .. main import project_flags
from .. util import data_file, log
from .. animation.animation import Animation
from .. project import load
from .. project.aliases import ALIAS_MARKERS
from .. project.project import Project

MOVIE_SUFFIXES = '.gif', '.mp4', '.yml'
_RUNNING = False


def stop():
    global _RUNNING
    _RUNNING = False
    Project.stop_all()


def run(args):
    Animation.FAIL_ON_EXCEPTION = args.fail_on_exception

    args.name = args.name or ['']
    projects = _get_projects(args)

    if args.dry_run:
        log.printer('(dry run - nothing executed)')
        return

    global _RUNNING
    _RUNNING = True

    needs_pause = False
    assert len(projects) == len(args.name)
    is_movie = (args.movie != '')

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
        if is_movie:
            project.flat_out()

        try:
            project.run()

        except KeyboardInterrupt:
            if not args.ignore_exceptions:
                raise
            log.warning('\nKeyboardInterrupt terminated project.')
            needs_pause = False

        except Exception:
            if not args.ignore_exceptions:
                raise
            log.exception('Exception')
            traceback.print_exc()


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

    movie = args.gif if args.movie == '' else args.movie
    if movie != '':
        log.info('writing animated movies')
        if movie is None:
            # --movie appeared but without a value
            movie = {}
        elif '{' in movie:
            movie = data_file.loads(movie, filename='--movie')

        if isinstance(movie, str):
            movie = {'filename': movie}
        filename = movie.get('filename', None)
        if filename:
            if not any(filename.endswith(s) for s in MOVIE_SUFFIXES):
                log.warning('--movie argument %s didn\'t end with %s',
                            movie, ' or '.join(MOVIE_SUFFIXES))
                movie += '.gif'
            if len(args.name) > 1:
                log.warning('Writing multiple movies to the same file name')

        movie['typename'] = '.movie_writer'

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
        root_file = None
        try:
            for filename in project_files.split('+'):
                if filename.endswith('.py'):
                    desc = _load_py(filename)
                    root_file = filename
                elif '{' in filename:
                    desc = data_file.loads(filename)
                elif '.' in filename:
                    desc = load.data(filename, False)
                    desc = data_file.load(desc, filename)
                    root_file = filename
                else:
                    raise ValueError('Do not understand command ' + filename)

                descs.append(desc)

            if movie:
                for d in descs:
                    d.pop('driver', None)
                if 'filename' in movie:
                    driver = movie
                else:
                    f = project_files.replace('+', '-')
                    f = f.replace('/', '-')
                    f = ''.join(i for i in f if i in _FILE_CHARS)
                    f, ext = os.path.splitext(f)
                    driver = dict(movie, filename=f + '.gif')
                descs.append({'driver': driver})

            project = project_flags.make_project(
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
            log.error('\n'.join(str(a) for a in args) + '\n')
        else:
            log.error(msg + '\n')
    raise ValueError('Run aborted')


_ALL_CHARS = set(string.ascii_letters + string.digits + '._' + ALIAS_MARKERS)
_START_CHARS = set(string.ascii_letters + '.' + ALIAS_MARKERS)
_END_CHARS = set(string.ascii_letters + string.digits)
_FILE_CHARS = set(string.ascii_letters + string.digits + '._-')


RUN_ERROR = """When reading file {filename}:

{desc}
{exception}
"""

FAILURE_ERROR = """\
{count} project{s} failed
____________________
"""


def _might_be_classname(s):
    return (s and
            set(s) <= _ALL_CHARS and
            s[0] in _START_CHARS and
            s[-1] in _END_CHARS)
