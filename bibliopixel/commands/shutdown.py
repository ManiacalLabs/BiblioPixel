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

from .. util.signal_handler import make_command
add_arguments, run = make_command('SIGINT')
