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

from . import restart


def set_parser(parser):
    restart.add_arguments(parser, 'SIGKINT')
