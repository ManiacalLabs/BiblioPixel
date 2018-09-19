0. Before you start
------------------------------


You don't need to know how to program in order to use BiblioPixel but you do need to
be familiar with a few things:

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

3. Either the YAML or JSON data file formats
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

BiblioPixel represents lighting Projects as text files in one of two formats -
`YAML <https://github.com/darvid/trine/wiki/YAML-Primer>`_
or `JSON <https://json.org>`_\ .

Most of our examples are in YAML, because it's less typing - however, many
people who write Javascript prefer JSON and that works perfectly well too.

BiblioPixel doesn't care about which file names you use, but it's neater to put
JSON data in files ending in .json and YAML data in files ending in .yml.

You can learn YAML by example, from reading this document.  If you're interested
in a bit more information, here's
`a link <https://github.com/darvid/trine/wiki/YAML-Primer>`_\ .

**Example 1**\ : Some data in JSON:

.. code-block:: json

    {
        "animation": {
            "typename": "sequence",
            "length": 3,
            "animations": [
                ".tests.PixelTester",
                {
                    "typename": "fill",
                    "color": "red"
                },
                "$bpa.matrix.MatrixRain"
            ]
        },
        "shape": [32, 32]
    }


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/0-example-1.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/0-example-1.gif
   :alt: Result


**Example 2**\ :  The same data in YAML:

.. code-block:: yaml

   # This is a comment.

   animation:
     typename: sequence
     length: 3

     animations:
       - .tests.PixelTester
       - {typename: fill, color: red}
       - $bpa.matrix.MatrixRain

   shape: [32, 32]


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/0-example-2.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/0-example-2.gif
   :alt: Result


YAML isn't just shorter and cleaner, it lets you write comments to yourself or
anyone else reading - by starting a line with the ``#`` character.

We're going to make heavy use of this "comment" feature in this documentation,
and we suggest you do too when writing your own lighting projects, unless your
memory is better than ours.

4. About the animated GIFs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Those pretty pictures are automatically generated from the example BiblioPixel
projects embedded in the documentation, so they fairly faithfully represent the
results you would get.

The one big difference is that that the GIFs loop after ten seconds (to keep
their size down), where the real animation will keep playing forever.

They're embedded in the text as examples of how to make Projects, and there's
also a unique one at the bottom of each page just for fun, as a sort of gallery
of animations.

----

.. code-block:: yaml

   shape: [64, 16]
   animation: $bpa.matrix.Twinkle


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/0-footer.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/0-footer.gif
   :alt: Result
