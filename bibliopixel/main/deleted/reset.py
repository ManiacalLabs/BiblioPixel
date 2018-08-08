"""
Reset sections in the project defaults
"""

DESCRIPTION = """
Example:

``````
# Reset the layout and animation sections
$ bp default reset layout animation

# Reset all sections
$ bp default reset
``````
"""

from ... project import defaults


def run(args):
    defaults.reset_defaults(args.sections)


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.add_argument('sections', nargs='*')
