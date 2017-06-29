import json
from . import simpixel, arguments
from .. import log
from .. util import files

HELP = """
Run a project description file.
"""


def make_desc(name, is_json):
    if not name:
        return {}

    data = name if is_json else files.opener(name).read()
    try:
        return json.loads(data)
    except ValueError as e:
        e.args += tuple(['in %s' % name])
        raise


def make_animation(name, is_json, args):
    desc = make_desc(name, is_json)
    return arguments.make_animation(args, desc)


def run(args, settings):
    if args.simpixel:
        simpixel.open_simpixel(args.simpixel)
    elif args.s:
        simpixel.open_simpixel()
    make_animation(args.name, args.json, args).start()


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.description = 'Run specified BiblioPixel project from file or URL.'

    arguments.add_to_parser(parser)

    parser.add_argument(
        'name', nargs='?',
        help='Path project file - can be a URL or file system location',
        default='')

    parser.add_argument(
        '-j', '--json', action='store_true',
        help='Enter JSON directly as a command line argument.')
