"""
Run specified project from file or URL
"""

from .. main import project_flags
from .. project import project_runner
from .. util import signal_handler


def run(args):
    for i in signal_handler.run(args.pid_filename, project_runner.stop):
        project_runner.run(args)


def add_arguments(parser):
    parser.set_defaults(run=run)
    project_flags.add_arguments(parser)

    parser.add_argument(
        'name', nargs='*',
        help='Path project files - can be a URL or file system location')
