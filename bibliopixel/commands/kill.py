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

from .. util.signal_handler import make_command
add_arguments, run = make_command('SIGKILL')
