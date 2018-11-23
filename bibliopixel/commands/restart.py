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

from .. util.signal_handler import make_command
add_arguments, run = make_command('SIGHUP', ' Default SIGHUP restarts bp.')
