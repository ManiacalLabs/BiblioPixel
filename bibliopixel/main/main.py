import importlib, sys
from .. import commands

DEFAULT_COMMAND = 'run'
ERROR = 'No command entered!'
USAGE = """\
No command entered!
Valid commands are:

    %s

For help on each command, type
    bp <command> -h
""" % ', '.join(commands.COMMANDS)


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
            log.error(ERROR + USAGE)
            return -1

    module = importlib.import_module('bibliopixel.commands.' + command)
    if hasattr(module, 'main'):
        return module.main(argv)

    description = module.__doc__ + getattr(module, 'DESCRIPTION', '')

    from . args import set_args
    args = set_args(description, argv, module)
    args.run(args)


if __name__ == '__main__':
    sys.exit(main())
