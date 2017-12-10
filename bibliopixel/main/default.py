import json, sys
from .. project import merge, defaults

COMMANDS = 'list', 'reset', 'set'


def run(args):
    if args.action == 'list':
        if args.sections:
            raise ValueError('list takes no arguments')
        else:
            defaults.list_defaults()

    elif args.action == 'reset':
        defaults.reset_defaults(args.sections)

    elif args.action == 'set':
        defaults.set_defaults(args.sections)


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.description = DESCRIPTION
    parser.add_argument(
        'action', choices=COMMANDS, help=COMMAND_HELP,
        default='list', nargs='?')
    parser.add_argument('sections', nargs='*')


COMMAND_HELP = """\
list -- list all defaults.
Example:

    $ bp default list

reset -- reset some or all sections of the project defaults.
Example:

    # Reset the layout and animation sections
    $ bp default reset layout animation

    # Reset all sectionsn
    $ bp default reset

set -- set some or all sections of the project defaults.

Each argument to `bp default set` has to look like

"""

DESCRIPTION = """Set defaults for projects using JSON.

A Project is a JSON file or equivalently a Python dictionary that describes
a BibliopPixel installation.  The top-level keys in a Project are called the
sections and a Project might have the following sections:

    {sections}

Often some sections of your project correspond to hardware and thus rarely
change, so the `bp default` command allows you to set defaults so you
don't have to mention these from your project at all.

""".format(sections=', '.join(merge.PROJECT_SECTIONS))
