The ``bp`` program.
==========================

1. What is ``bp``\ ?
^^^^^^^^^^^^^^^^^^^^^^

``bp`` is short for the BiblioPixel project runner.  It's a command line
application that's installed as part of BiblioPixel, along with the
``bibliopixel`` Python library.

You've already used ``bp`` to run your BiblioPixel projects and ``bp new`` to
create a new BiblioPixel project, but ``bp`` has all sorts of other Commands,
with names like ``run``\ , ``new``\ , ``demo``\ , and ``animations``.

2. Built-in documentation for ``bp``.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``bp`` has its own "help" system:

.. code-block:: bash

   $ bp --help
   ## `bp` - The BiblioPixel Project Runner

   `bp` is a command-line script installed with Bibliopixel.  It can run
   projects and demos, configure hardware, save and load defaults, and more.
   [... more help ...]

You can also type ``bp -h``\ , ``bp help`` or just ``bp`` to get the same result.

If you want help on a specific Command, try this:

.. code-block:: bash

   $ bp --help animations

   usage: bp animations [-h]

   List all animations

   optional arguments:
     -h, --help            show this help message and exit

There's also a full set of online documentation for ``bp``
`here <../reference/The-bp-program.rst>`_.

3.  ``bp`` command lines
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's start with a few examples:

.. code-block:: bash

   $ bp
   $ bp color red
   $ bp animations

   $ bp one.yml
   $ bp run one.yml
   $ bp one.yml -vs --loglevel=frame
   $ bp one.yml+two.yml three.yml

   $ bp monitor midi

A ``bp`` command line has three parts, each optionalL


* the Command (e.g. ``color``\ )
* the Arguments (e.g. ``red`` or ``one.yml+two.yml three.yml``\ )
* the Flags (e.g. ``-vs --loglevel=frame``\ )

The Command defaults to ``run`` so ``bp one.yml`` and ``bp run one.yml`` are the same.

Some Commands take no arguments: ``bp animations``

Some Commands take exactly one argument:  ``bp color green``

Some Commands take one optional argument:  ``bp demo`` or ``bp demo cube``

Some Commands take one or more arguments: ``bp run one.yml two.yml``

4. How to stop or restart ``bp``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

While some Animations can have a specific, fixed length like ten seconds, most
of them go on indefinitely.  Sometimes you want to tell ``bp`` to stop running,
or you want to tell it to restart from the beginning again.


4.1. Control-C
~~~~~~~~~~~~~~~~~~~~~

The simplest way to stop ``bp`` is using Control-C - hold down the Control or
CTR key and press C

Control-C interrupts almost any command line program, not just ``BiblioPixel``.
It must be done in the command line which is running ``bp``.


4.2. Unix signals
~~~~~~~~~~~~~~~~~~~~~

This is an advanced section which can safely be skipped.

A more versatile way (which unfortunately does not work on Windows) is to send a
`Unix signal <https://www.tutorialspoint.com/unix/unix-signals-traps.htm>`_
to the ``bp`` process.

``bp`` understands three Unix signals:

``SIGINT``
  Shut ``bp`` down in a controlled fashion, turning off all lights:
  equivalent to typing Control-C.

``SIGTERM``
  Shut ``bp`` down immediately.

``SIGHUP``
  Stop the running ``bp`` Project in a controlled fashion, create a new
  Project by re-reading the originalo Project file, then run it.

``SIGHUP`` is particularly useful for developers who want to restart their
application with a new Animation without taking the several seconds it would
take to bring ``bp`` down and back up again.

A tiny bash utility ``bp-pid`` is installed with BiblioPixel to report on the
process ID that's running ``bp``.

For example, to send a ``SIGHUP`` to the running ``bp`` process, if any, use
this command line:

.. code-block:: bash

    $ kill -hup `bp-pid`

This will restart ``bp`` if it is running, otherwise cause an error.

----

.. code-block:: yaml

   shape: [64, 13]
   animation: $bpa.strip.LarsonScanners.LarsonRainbow


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/the-bp-program-footer.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/the-bp-program-footer.gif
   :alt: Result
   :align: center
