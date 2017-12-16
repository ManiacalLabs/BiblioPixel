from .. project import defaults


def run(args):
    defaults.reset_defaults(args.sections)


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.description = DESCRIPTION
    parser.add_argument('sections', nargs='*')


DESCRIPTION = """reset -- reset some or all sections of the project defaults.
Example:

    # Reset the layout and animation sections
    $ bp default reset layout animation

    # Reset all sectionsn
    $ bp default reset
"""
