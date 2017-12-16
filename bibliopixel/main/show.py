from .. project import defaults


def run(args):
    defaults.show_defaults()


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.description = 'Show all default values'
