Before you start
------------------------------

You don't have to program to use BiblioPixel but you do need to be know a couple
of things.

Using the command line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

BiblioPixel is a command line program: you run it by typing commands into a
terminal window and giving text responses. You don't have to be an
expert on the command line to use it for BiblioPixel!  You just need to be
comfortable with changing directories, entering commands and pressing return.

In this documentation, command lines are show starting with the dollar sign
character ``$`` - don't type the ``$`` yourself when entering command lines!

Try it now - open a terminal window and type:

.. code-block:: bash

    $ echo hello-world

This should print out the string ``hello-world`` on your terminal.


Using a text editor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

BiblioPixel uses text files to represent lighting Projects, so you'll need
a text editor to prepare your Projects.  (Microsoft Word won't work
- Word is a word processor, a very different sort of program.)

You don't need anything fancy.  Every computer comes with some sort
of simple, free text editor:

* ``Notepad`` on Windows
* ``Text`` on the Macintosh
* ``vi`` or ``emacs`` on Linux, Rasbperry Pi, Mac, Windows and almost all other
  platforms

There's also a popular commercial text editor named SublimeText, which also
works on almost all platforms.

.. bp-code-block:: footer

   shape: [64, 16]
   animation:
     typename: $bpa.matrix.Twinkle
     speed: 5
     density: 100
