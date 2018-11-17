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


def add_arguments(parser):
    restart.add_signal_arguments(parser, 'SIGKILL')
