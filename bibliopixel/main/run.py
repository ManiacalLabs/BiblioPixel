from bibliopixel.util import project

HELP = """
Run a project description file.
"""


def run(args):
    data = args.name and open(args.name).read() or {}
    project.run(data)


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.add_argument('name', nargs='?')
