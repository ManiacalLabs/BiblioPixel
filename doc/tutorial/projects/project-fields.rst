More on Fields
-------------------


A Project is made up of *Sections*, and Sections have *Fields*.
================================================================

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

The Value Sections are ``aliases``, ``numbers``, ``palettes``, ``path``,
``run``, and ``shape``.

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

**Example 1**:  An Animation that runs a simple test on a strip of 32 pixels

.. bp-code-block:: example-1

   shape: 32
   animation:
       typename: .tests.PixelTester


On the other hand, the ``.sequence`` Animation requires a Field ``animations``,
a list of Animations that are played in sequence.  It also has an optional
Field ``length`` which sets the length of each subsequence.

**Example 2**:  This Animation runs four Animations, each for two seconds, in a
  loop, and displays the result on a 32x32 pixel display.

.. bp-code-block:: example-2

   shape: [32, 32]

   animation:
       typename: .sequence
       length: 2
       animations:
           - $bpa.matrix.ImageAnim
           - $bpa.matrix.ImageShow
           - $bpa.matrix.ImageDissolve
           - $bpa.matrix.ScreenGrab


.. bp-code-block:: footer

   shape: [64, 11]
   animation: $bpa.strip.HalvesRainbow
