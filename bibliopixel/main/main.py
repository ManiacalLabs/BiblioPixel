import sys
from . import args, commands, common_flags
from .. util import log
from .. project import aliases, project

__all__ = ['main']


def main():
    args.parse_args(commands, common_flags)
    run = getattr(args.ARGS, 'run', None)
    if not run:
        log.printer('ERROR: No command entered')
        log.printer('Valid commands are:')
        log.printer('    ', ', '.join(commands.COMMANDS))
        log.printer()
        log.printer('For more help, type')
        log.printer()
        log.printer('    bp --help')
        sys.exit(-1)

    common_flags.execute_args(args.ARGS)

    try:
        result = run(args.ARGS) or 0
    except Exception as e:
        if args.ARGS.verbose:
            raise
        log.printer('ERROR:', e.args and e.args[0], file=sys.stderr)
        log.printer(*e.args[1:], sep='\n', file=sys.stderr)
        result = getattr(e, 'errorcode', -1)

    sys.exit(result)
