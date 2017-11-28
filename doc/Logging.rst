BiblioPixel provides an information and debug logging system via the
built-in Python
`logging <https://docs.python.org/2/library/logging.html>`__ module. To
enable the ability to turn built-in debugging information about the
BiblioPixel classes, an internal wrapper located in *bibliopixel.log*.

To enable these debug messages, insert the following code at the top of
your script:

.. code:: python

    from bibliopixel import log
    log.setLogLevel(log.DEBUG)

Doing so and running an animation will cause it to output the following
on every step:

::

    DEBUG - animation - 4ms/250fps / Frame: 2ms / Update: 2ms

The above is used for debugging animation/driver performance and breaks
down as: \* DEBUG - Log level of the message. \* animation - Module the
message originated from. \* 4ms/250fps - Total time (ms) the frame
required / Effective frame rate. \* Frame: 2ms - Time required to render
frame \* Update: 2ms - Time required to push frame to display.

The following log levels are available: \* DEBUG \* INFO \* WARNING \*
ERROR \* CRITICAL

Calling log.setLogLevel() with one of these with cause all messages with
that level, or higher, to be output. DEBUG being the lowest and CRITICAL
being the highest. BiblioPixel defaults to INFO, which is used for basic
system messages, if needed.

To output to the log, use the following methods: \*
log.logger.debug(str) \* log.logger.info(str) \* log.logger.warning(str)
\* log.logger.error(str) \* log.logger.critical(str)

For convenience, the ERROR and CRITICAL log messages are automatically
placed on the stderr stream so that they can be more easily separated
from normal output.
