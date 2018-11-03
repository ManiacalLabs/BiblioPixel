The ``bp`` program.
==========================

``bp`` is the BiblioPixel project runner, a command line application installed
as part of BiblioPixel.

``bp``

You've already used ``bp`` to run your BiblioPixel projects and ``bp new`` to
create a new BiblioPixel project, but ``bp`` has all sorts of other Commands,
with names like ``run``, ``new``, ``demo``, and ``animations``.

2. Built-in documentation for ``bp``.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``bp`` has its own "help" system:

.. code-block:: bash

   $ bp --help
   ## `bp` - The BiblioPixel Project Runner

   `bp` is a command-line script installed with Bibliopixel.  It can run
   projects and demos, configure hardware, save and load defaults, and more.
   [... more help ...]

You can also type ``bp -h``, ``bp help`` or just ``bp`` to get the same result.

If you want help on a specific Command, try this:

.. code-block:: bash

   $ bp --help animations

   usage: bp animations [-h]

   List all animations

   optional arguments:
     -h, --help            show this help message and exit

There's also a full set of online documentation for ``bp``
`here <../reference/The-bp-program>`_.

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

A ``bp`` command line has three parts, each optional:


* the Command (e.g. ``color``)
* the Arguments (e.g. ``red`` or ``one.yml+two.yml three.yml``)
* the Flags (e.g. ``-vs --loglevel=frame``)

The Command defaults to ``run`` so ``bp one.yml`` and ``bp run one.yml`` are the
same.

Commands can take any number of arguments - examples:

* no arguments: ``bp animations``
* exactly one argument:  ``bp color green``
* one optional argument:  ``bp demo`` or ``bp demo cube``
* one or more arguments: ``bp run one.yml two.yml``

.. bp-code-block:: footer

   shape: [64, 13]
   animation:
     typename: $bpa.matrix.circlepop
     palette: warm
