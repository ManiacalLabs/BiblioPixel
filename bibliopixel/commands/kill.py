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

from . import restart


def set_parser(parser):
    restart.add_arguments(parser, 'SIGKILL')
