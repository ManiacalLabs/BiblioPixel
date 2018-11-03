How to write a Project
-----------------------------

This page guides you through creating a new project from scratch.


1. Open a command line and hange directory to the directory you want to work in
================================================================================

Often you'd want to work in your home directory:

.. code-block:: bash

   cd ~

3. Use the ``bp new <your-project-name>`` to create a new project
=============================================================================

Suppose you want to call your project ``my_lights``

.. code-block:: bash

   bp new my_lights

This will create a new directory named ``my_lights/`` in your current
directory which contains a sample project file and a sample Python file for you
to edit.

4. Run the Project file:
========================

Change directory to the project directory, and run the Project file, like this:

.. code-block:: bash

   cd my_lights
   bp -s my_lights.yml

The ``-s`` flag to ``bp`` means "open a SimPixel window" and it will indeed open
on your browser, showing a lighting pattern like this:

.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-1.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-1.gif
   :alt: Result
   :align: center

5.  Stop the program.
=====================

Press control-c to stop the ``bp`` program.
