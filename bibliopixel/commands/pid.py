"""
Print the process ID of the current bp instance that is running a project,
if any.

DEPRECATED: use ``$ bpa-pid``
"""

DESCRIPTION = """
Example:

.. code-block:: bash

    $ bp pid

"""

from .. util import log, pid_context


def run(args):
    try:
        log.printer(pid_context.get_pid(args.pid_filename))
    except:
        log.error('No bp process running')
        log.debug('Could not find file %s', args.pid_filename)
        return -1


def set_parser(parser):
    parser.set_defaults(run=run)
