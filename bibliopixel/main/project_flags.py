from .. project import data_maker, defaults, project
from . import common_flags
from .. util import data_file, deprecated, log, pid_context

"""Common command line arguments for run and demo."""


COMPONENTS = 'driver', 'layout', 'animation'
PRESET_LIBRARY_DEFAULT = '~/.bibliopixel'
ENABLE_PRESETS = False
NUMBER_TYPES = ('python',) + data_maker.NUMPY_TYPES


def add_arguments(parser):
    pid_context.add_arguments(parser)

    parser.add_argument(
        '-a', '--animation', default=None,
        help='Default animation type if no animation is specified')

    parser.add_argument(
        '-b', '--brightness', default=None,
        help='Override project brightness value')

    parser.add_argument(
        '-d', '--defaults', default=None, nargs='*',
        action='append', help='Use this default setting')

    if deprecated.allowed():  # pragma: no cover
        parser.add_argument(
            '--dimensions', '--dim', default=None,
            help='DEPRECATED: x, (x, y) or (x, y, z) dimensions for project')

    parser.add_argument(
        '--shape', default=None,
        help='x, (x, y) or (x, y, z) dimensions for project')

    parser.add_argument(
        '--dump', action='store_true',
        help='Dump the full project as DATA_FILE after loading but ' +
             'before running')

    parser.add_argument(
        '--dry_run', action='store_true',
        help='Load projects but do not run them')

    parser.add_argument(
        '-f', '--fail_on_exception', action='store_true',
        help='If true, bp fail if any subanimation fails to construct')

    if deprecated.allowed():
        parser.add_argument(
            '-g', '--gif', default='', nargs='?', help=GIF_HELP)

    parser.add_argument(
        '-i', '--ignore_exceptions', action='store_true',
        help='If true, continue running the next project if one project fails')

    parser.add_argument(
        '-j', '--json', action='store_true',
        help='Use Json when dumping description data')

    parser.add_argument(
        '-l', '--layout', default=None,
        help='Default layout class if no layout is specified')

    parser.add_argument(
        '-m', '--movie', default='', nargs='?', help=MOVIE_HELP)

    parser.add_argument(
        '--numbers', '-n', default='python', choices=NUMBER_TYPES,
        help=NUMBERS_HELP)

    parser.add_argument('-p', '--path', default=None, help=PATH_HELP)

    parser.add_argument(
        '--pause', default=0, help='Time to pause between running animations')

    parser.add_argument(
        '--project_lengths', '--pl', default=None, help=PROJECT_LENGTHS_HELP)

    parser.add_argument(
        '-s', action='store_true', help='Run SimPixel at the default URL')

    parser.add_argument(
        '--simpixel', help='Run SimPixel at a specific URL')

    parser.add_argument(
        '--animation_lengths', '--at', default=None,
        help='Set run length for each animation')

    parser.add_argument(
        '-t', '--ledtype', default=None,
        help='Default LED type if no LED type is specified')


def _make_project_flags(args):
    def get_value(name):
        value = getattr(args, name, None)
        if not value:
            return {}

        if '{' in value:
            return data_file.loads(value)

        return {'typename': value}

    project_flags = {name: get_value(name) for name in COMPONENTS}
    if args.ledtype:
        project_flags['driver']['ledtype'] = args.ledtype

    if args.brightness:
        project_flags['layout']['brightness'] = int(args.brightness)

    if args.defaults:
        # Arguments come in like: [['foo'], ['bar'], ['baz'], ...]
        # I have no idea why.
        defs = [(a[0] if isinstance(a, list) else a) for a in args.defaults]
        defaults.set_project_defaults(defs)

    if args.v4:
        log.printer('*** Using v4 forward compatibility mode.')
        project_flags['numbers'] = 'float'
    elif args.numbers != 'python':
        project_flags['numbers'] = args.numbers

    if args.project_lengths is not None:
        run = project_flags.setdefault('run', {})
        run['seconds'] = float(args.project_lengths)

    if args.animation_lengths is not None:
        animation = project_flags.setdefault('animation', {})
        length = [float(i) for i in args.animation_lengths.split(',')]
        animation['length'] = length

    if args.dimensions is not None:
        deprecated.deprecated('Use --shape: --dimensions')

    shape = args.shape or args.dimensions
    if shape is not None:
        shape = shape.split(',')
        try:
            project_flags['shape'] = [int(i) for i in shape]
        except:
            raise ValueError('--shape must be one to three numbers '
                             'separated by commas.')

    return project_flags


def make_project(args, *descs, root_file=None):
    project_flags = _make_project_flags(args)
    descs += (project_flags,)
    return project.project(*descs, root_file=root_file)


# Help messages.

PATH_HELP = """\
A list of directories, separated by colons, 'which are added to the end of
`sys.path`.

You can also use loady-style paths which start with `//git/` to
dynamically load a library from a public git repository.

See https://github.com/ManiacalLabs/BiblioPixel/wiki/BiblioPixel-Paths
for more information.
"""

NUMBERS_HELP = """
The type of numbers that are used in color list calculations.

  `python` means to use the classic Python lists of (r, g, b) tuples.

  Anything else is a numpy type, which means that bp uses numpy arrays, which
  use much faster arithmetic.

  numpy types include:
    """ + ' '.join(data_maker.NUMPY_TYPES)

PRESET_HELP = """Filenames for preset library"""

PROJECT_LENGTHS_HELP = """\
How long to run the animation (overrides runner.seconds)"""

MOVIE_HELP = """
Write a movie file (animated GIF or mp4).

If --gif has no argument, the name of the movie file is the same as the name of
the project, with a .gif added to the end.

If it has a single string argument, then it's the name of the GIF file.

Otherwise, the argument is read as JSON and used to construct a GifWriter class.
"""

# TODO: this should go somewhere else
"""
Set defaults for projects using YAML or JSON data files.

A Project is a data file or equivalently a Python dictionary that describes
a BibliopPixel installation.  The top-level keys in a Project are called the
sections and a Project might have the following sections:

    {sections}

Often some sections of your project correspond to hardware and thus rarely
change, so the `bp default` command allows you to set defaults so you
don't have to mention these from your project at all.
"""

GIF_HELP = """
--gif/-g is a deprecated name for the --movie/-m flag."
""" + MOVIE_HELP
