How to run the documentation build
--------------------------------------

1. Initial setup.
===============================

There are four different git branches needed for building BiblioPixel
documentation, and all they need to be checked out in the same directory:

.. code-block:: bash

   <root directory>
       BiblioPixel            # master, dev or docs branch
       BiblioPixel.gh-pages   # gh-pages branch
       DocsFiles              # master branch
       BiblioPixelAnimations  # master branch

2. Building the documentation
=====================================

The documentation scripts are in the ``scripts/documentation``
directory, and all BiblioPixel scripts are intended to be run
from the BiblioPixel root directory.

``clean``
  Delete all existing documentation files

``api``
  Automatically generate API documentation to the file
  ``BiblioPixel/doc/reference/api``

``bp``
  Automatically generate documentation for the `bp` command line
  program to the file  ``BiblioPixel/doc/The-bp-command.rst``

``extract-gifs``
  Extract GIFs whose projects are in documentation or code into the
  directory ``DocsFiles/BiblioPixel``

``sphinx``
  Run the Sphinx build into the directory ``BiblioPixel.gh-pages/html``

``deploy``
  Commit and push any changes to ``DocsFiles/BiblioPixel`` and
  ``BiblioPixel.gh-pages/html``

``build``
  Equivalent to ``clean && api && bp && extract-gifs && sphinx``
