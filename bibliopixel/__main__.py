import platform

MINIMUM_VERSION = '3.4.0'

if platform.python_version() < MINIMUM_VERSION:
    raise EnvironmentError(
        '%s needs Python %s or later: your Python version is %s' % (
            __package__, MINIMUM_VERSION, platform.python_version()))

try:
    import argparse
    import argcomplete
    import sys
    from bibliopixel import __description__, __url__
    from bibliopixel.cli import get_available_commands
except ImportError:  # pragma: no cover
    err = sys.exc_info()[1]
    raise ImportError(str(err))


def main():
    status = 0
    parser = argparse.ArgumentParser(prog=__package__,
                                     description=__description__,
                                     epilog="More info available at: {}".format(__url__))
    subparsers = parser.add_subparsers(title="Commands", description="")

    for cmd in get_available_commands():
        cmd.create_parser(subparsers)

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if hasattr(args, 'command_class'):
        status = args.command_class(args).run()
    else:
        parser.print_help()

    sys.exit(status)


if __name__ == "__main__":
    main()
