from bibliopixel.project import project
from bibliopixel.util import opener

HELP = """
Run a project description file.
"""


def run(args, settings):
    data = args.name and opener.opener(args.name).read() or {}
    project.run(data)


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.description = 'Run specified BiblioPixel config from file'
    parser.add_argument('name', nargs='?', help='Path to config json file')
