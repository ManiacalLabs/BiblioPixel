from .. project import defaults


def run(args):
    defaults.list_defaults()


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.description = 'Show all default values'
