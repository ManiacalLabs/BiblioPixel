4. Projects
===========

A BiblioPixel Project is a text file describing a lighting project in either
`YAML <https://yaml.org>`_ or `JSON <https://json.org>`_ format.

Projects have been designed to be as flexible and forgiving as possible.

You can reuse bits of projects inside other projects, and you can combine
partial projects from the command line, like this:

.. code-block:: yaml

    bp living-room.yml + smooth-fades.yml

    # Or even inline
    bp smooth-fades.yml + '{shape: [30, 30], driver: my-driver.yml}'

You have many formats you can use for values - for example, you can represent
colors by a name like ``"red"`` or ``"DarkSlateBlue"``, a web color like
``#FF7F0F``, or a list of RGB components like ``[255, 127, 15]``.

There's every attempt to give good error messages, and to explain that, for
example, ``"sickly pink"`` is not a valid color name.

If you run into an error message using Projects that you do not understand,
please report it as an issue
`here <https://github.com/ManiacalLabs/BiblioPixel/issues>`_
or ask a question on the
`Maniacal Labs User Group <https://groups.google.com/d/forum/maniacal-labs-users>`_\ .

**Example 1** : a simple Project file written in YAML

.. code-block:: yaml

   shape: 50
   animation: $bpa.strip.Wave


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/4-example-1.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/4-example-1.gif
   :alt: Result


**Example 2** : a slightly larger Project file, written in JSON

.. code-block:: json

   {
       "shape": [32, 32],

       "run": {
           "fps": 60
       },

       "animation": {
           "typename": "$bpa.matrix.MatrixRain",
           "colors": ["blue", "yellow", "coral"]
       }
   }


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/4-example-2.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/4-example-2.gif
   :alt: Result


**Example 3** : the same Project file as in Example 2, but written in YAML

.. code-block:: yaml

   shape: [32, 32]

   run:
     fps: 60

   animation:
     typename: $bpa.matrix.MatrixRain
     colors: [blue, yellow, coral]


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/4-example-3.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/4-example-3.gif
   :alt: Result


A Project is made up of *Sections*, and Sections have *Fields*.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Project files can have as many as ten Sections, but nearly all the Sections are
optional.

The Project files above contain three Sections: ``shape``, ``run``, and
``animation``, and the ``animation`` Section contains two Fields, ``typename``
and ``colors``.

The Project Sections are ``aliases``, ``animation``, ``controls``, ``driver``,
``drivers``, ``layout``, ``numbers``, ``path``, ``run``, and ``shape``... but
you will probably never use many of these.

Sections can have Fields - for example, the ``run`` Section above has the Field
``fps: 60``.

The most important Sections are ``animation``, ``shape``, and ``driver``, which
appear in almost every Project:


``animation``
    a program that changes your lights over time

``shape``
    shows how your lights are laid out in 1, 2, or 3 dimensions

``driver``
    configures and runs the driver that controls the actual lights


Class Sections and Value Sections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sections naturally fall into two categories.

*Value Sections* are fairly simple things like strings, numbers, lists, or
dictionaries.

The five Value Sections are ``aliases``, ``numbers``, ``path``, ``run``, and
``shape``.

*Class Sections* represent Python objects - actual programs. Nearly all the
excitement in BiblioPixel is in the Class Sections!

There are five Class Sections:
``animation``, ``controls``, ``driver``, ``drivers`` and ``layout``.

Each Class Section has a special Field ``typename`` containing the name of its
Python Class.

The Python Class determines what that Section does, and which Fields can be set
on it.  The ``typename`` field lets you load not just BiblioPixel code, but your
own code or third-party code.

BiblioPixel comes with a large number of predefined Animations, Controls,
Drivers and Layouts, and you can put them together and customize them simply by
writing a Project, without any programming.

More, if you know a little Python you can extend them or modify a copy, or just
write your own from scratch.

More on Fields
~~~~~~~~~~~~~~~~~~~~~~~~~

Each Section has named *Fields* - values that you can set in that Section.

In Example 2 and 3 above, the ``run`` Section has the Field ``fps`` with value
``60`` (fps meaning "frames per second"), and the ``animation`` Section has the
Field ``imagePath`` with value ``/Users/tom/Documents/giphy-zoom.gif``.

A Value Section always has the same Fields - for example, the ``run`` Section
always has the ``fps`` Field in any Project.

On the other hand, a Class Section will have different Fields depending on its
``typename``.

For example, many Animations have no Fields at all and do exactly one thing,
like the Animation ``.tests.PixelTester``:

**Example 4**:  An Animation that runs a simple test on a strip of 32 pixels

.. code-block:: yaml

   shape: 32
   animation:
       typename: .tests.PixelTester


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/4-example-4.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/4-example-4.gif
   :alt: Result


On the other hand, the ``.sequence`` Animation requires a Field ``animations``,
a list of Animations that are played in sequence.  It also has an optional
Field ``length`` which sets the length of each subsequence.

**Example 5**:  This Animation runs four Animations, each for two seconds, in a
  loop, and displays the result on a 32x32 pixel display.

.. code-block:: yaml

   shape: [32, 32]

   animation:
       typename: .sequence
       length: 2
       animations:
           - $bpa.matrix.ImageAnim
           - $bpa.matrix.ImageShow
           - $bpa.matrix.ImageDissolve
           - $bpa.matrix.ScreenGrab


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/4-example-5.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/4-example-5.gif
   :alt: Result


A quick description of each section
--------------------------

Class Sections
~~~~~~~~~~~~~~~

``driver``
    The output driver: converts to a hardware, software or simulator output.

``drivers``
    Used if there's more than one Driver.  If the ``drivers`` Section
    is non-empty, the ``driver`` Section becomes a template for ``drivers``.

``layout``
    Lays the lights out geometrically.

``animation``
    Animates the lights over time.

``controls``
    Classes that use external input to control parts of  the Project.


Value Sections
~~~~~~~~~~~~~~

``aliases``
    A dictionary of aliases that are expanded in ``typename`` fields
    to save repetition in Project files.

``numbers``
    Selects between plain old Python lists and faster, more powerful ``numpy``
    lists.

``path``
    ``path`` is added to the ``PYTHONPATH`` to allow loading of local Python
    libraries.

``run``
    Controls how the topmost Animation is executed - how fast it runs, for how
    long or for how many times, and more.

``shape``
    The shape of the layout - ``length`` for strips, ``[width, height]`` for
    matrices and ``[x, y, z]`` for cubes.


----

.. code-block:: yaml

   shape: [64, 4]
   animation: $bpa.strip.LarsonScanners.LarsonScanner


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/4-footer.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/4-footer.gif
   :alt: Result
