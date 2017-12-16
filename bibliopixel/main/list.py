from .. project import defaults


def run(args):
    defaults.list_saved_defaults()


def set_parser(parser):
    parser.set_defaults(run=run)
    parser.description = 'List all saved defaults settings'
