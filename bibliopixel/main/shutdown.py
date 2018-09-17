"""
Send an interrupt signal to a BiblioPixel process running on this
machine to kill it

DEPRECATED: use
.. code-block:: bash

    $ kill -int `bpa-pid`

"""

DESCRIPTION = """
Example:
`$ bp shutdown`

"""

from . restart import run, CHOICES


def set_parser(parser):
    parser.add_argument(
        'signal', nargs='?', default='SIGINT', choices=CHOICES,
        help='Signal to send.')

    parser.set_defaults(run=run)
