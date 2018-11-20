"""
Run specified project from file or URL
"""

from .. main import project_flags
from .. project import project_runner
from .. util import log, pid_context, signal_handler

SIGNALS = 'SIGHUP', 'SIGINT', 'SIGTERM'
SIGNAL_DICT = {s: project_runner.stop for s in SIGNALS}


def run(args):
    with pid_context.pid_context(args.pid_filename):
        with signal_handler.context(**SIGNAL_DICT) as signals:
            while True:
                project_runner.run(args)
                if signals:
                    log.info('Received signal %s', ' '.join(signals))

                if not signals.pop('SIGHUP', False):
                    break


def add_arguments(parser):
    parser.set_defaults(run=run)
    project_flags.add_arguments(parser)

    parser.add_argument(
        'name', nargs='*',
        help='Path project files - can be a URL or file system location')
