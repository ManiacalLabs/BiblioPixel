Before you start
------------------------------


You don't need to know how to program in order to use BiblioPixel but you do need to
be familiar with a couple of things:

1. Using the command line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

BiblioPixel is a command line program, run by typing commands into a terminal
window and giving text responses.

You don't by any means have to be an expert on the command line to use it for
BiblioPixel!  You just need to be comfortable with entering commands and
pressing return, and with the idea of directories and the current directory.

In this documentation, lines that you type into a command line will start
with the dollar sign character ``$`` to distinguish them from the results -
so don't type the ``$`` yourself when entering command lines.

Try it now - open a terminal window and type:

.. code-block:: bash

    $ echo hello-world

This should print out the string ``hello-world`` on your terminal.


2. Using a text editor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

BiblioPixel uses text files to represent lighting Projects, and so you will need
some sort of text editor to prepare your Projects.

You don't need anything too sophisticated.  Every computer comes with some sort
of simple, free text editor:

* ``Notepad`` on Windows
* ``Text`` on the Macintosh
* ``vi`` or ``emacs`` on Linux, Rasbperry Pi and almost all other platforms

A popular text editor, SublimeText, works on all these platforms.

NOTE: Microsoft Word does not work for this task of text editing - it's a word
processor, a different sort of program, and it embeds all sorts of other
information in its documents which BiblioPixel cannot process.

----

.. code-block:: yaml

   shape: [64, 16]
   animation:
     typename: $bpa.matrix.Twinkle
     speed: 5
     density: 100

.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/before-you-start-footer.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/before-you-start-footer.gif
   :alt: Result
   :align: center
