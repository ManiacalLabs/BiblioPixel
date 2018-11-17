"""
Send a restart signal to a BiblioPixel process running on this
machine.

DEPRECATED: use

.. code-block:: bash

    $ kill -hup `bpa-pid`


"""

DESCRIPTION = """
Example: ``$ bp restart``

"""

import os, signal
from .. project import defaults
from .. util import log, pid_context

CHOICES = sorted(d for d in dir(signal) if d.startswith('SIG') and '_' not in d)


def run(args):
    try:
        pid = pid_context.get_pid(args.pid_filename)
    except:
        log.error('No bp process running')
        log.debug('Could not find file %s', args.pid_filename)
        return -1

    try:
        os.kill(pid, getattr(signal, args.signal))
    except:
        log.error('Failed to send signal %s to bp process %s', args.signal, pid)
        return -1

    log.info('%s sent to bp process %s', args.signal, pid)


def add_signal_arguments(parser, default, help=''):
    parser.add_argument(
        'signal', nargs='?', default=default, choices=CHOICES,
        help='Signal to send.' + help)
    pid_context.add_arguments(parser)
    parser.set_defaults(run=run)


def add_arguments(parser):
    add_signal_arguments(parser, 'SIGHUP', ' Default SIGHUP restarts bp.')
