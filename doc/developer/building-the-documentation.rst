Building the documentation
===============================

The Python documentation world is a little janky and so there is also a
separate build for the documentation part!

If you make significant changes to the documentation, you'll need to learn how
to run this documentation build so you can see your results.

We use the powerful but gnarly `Sphinx <http://www.sphinx-doc.org/en/master/>`_
documentation system for Python.  You won't have to read that previous link, we
hope, because that has mostly been automated away.

Documentation files are in the doc/ subdirectory and are in the poorly-specified
but fairly easy to understand `reStructuredText format.
<http://docutils.sourceforge.net/rst.html>`_

There are multiple parts to building the documentation, though they are all
automated:

1. The preprocessing phase
2. Extracting the API documentation
3. Extracting the documentation on the ``bp`` command
4. Running Sphinx to convert the documentation into HTML files
6. GIF extraction and deployment (see next page)


The basic Build
========================

To build the documentation, go to the BiblioPixel directory and run one of the
build scripts:

.. code-block:: bash

    $ scripts/documentation/build

This runs preprocessing + api + bp + sphinx.  Use this if you have changed both
the Python code and the documentation, or the very first time you want to build
documentation.

To actually look at the documentation, go the ``html`` directory in the base
``BiblioPixel`` directory and open the file ``index.html`` in your browser
(which you can probably do just by double-clicking on it).

.. code-block:: bash

    $ scripts/documentation/quick_build

This runs preprocessing + bp + sphinx.

Running the api task is quite slow, and if you haven't made changes to the
Python source code, since the last time you did a full build, it's unnecessary.

``quick_build`` is what you will use most of the time.

.. code-block:: bash

    $ scripts/documentation/clean

This cleans out all the existing documentation build.  You should do this if you
have made major changes to the structure and want to get rid of old files;  but
it won't cause issues for anyone else if you don't run this, as it's purely
local.
