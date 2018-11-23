import importlib, sys
from .. import commands


def main(argv=None):
    argv = sys.argv[1:] if argv is None else list(argv)

    for i, arg in enumerate(argv):
        if arg in commands.COMMANDS:
            command = argv.pop(i)
            break
    else:
        command = DEFAULT_COMMAND
        if all(a.startswith('-') for a in argv):
            from .. util import log
            if '-h' in argv or '--help' in argv:
                log.printer(USAGE)
                return 0

            log.error(ERROR + '\n\n' + USAGE)
            return -1

    module = importlib.import_module('bibliopixel.commands.' + command)
    if hasattr(module, 'main'):
        return module.main(argv)

    description = module.__doc__ + getattr(module, 'DESCRIPTION', '')

    from . args import set_args
    args = set_args(description, argv, module)
    module.run(args)


DEFAULT_COMMAND = 'run'
ERROR = 'No command entered!'
USAGE = """Valid commands are:

""" + commands.COMMANDS_PRINTABLE + """

For help on each command, type

    bp <command> --help

or

    bp <command> -h
"""


if __name__ == '__main__':
    sys.exit(main())
