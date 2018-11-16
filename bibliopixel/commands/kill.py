"""
Send a kill signal to a BiblioPixel process running on this
machine to abruptly kill it

DEPRECATED: use

.. code-block:: bash

    $ kill -kill `bpa-pid`

"""

DESCRIPTION = """
Example:

.. code-block:: bash

    $ bp kill

"""

from . restart import run, CHOICES


def set_parser(parser):
    parser.add_argument(
        'signal', nargs='?', default='SIGKILL', choices=CHOICES,
        help='Signal to send.')

    parser.set_defaults(run=run)
