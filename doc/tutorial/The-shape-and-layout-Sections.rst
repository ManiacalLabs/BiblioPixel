The ``shape`` and ``layout`` Sections.
----------------------------------------------

The ``shape`` Value Section is a simple way of representing how your lights are
actually laid out in the real world.  The ``layout`` Class Section lets you
represent more complicated setups.

``shape``
==============

``shape`` specifies how many lights there are and how they are arranged.

If the lights are in a linear strip, ``shape`` is a single number.  For example,
if you have 100 LEDs, your Project will contain a line like:

.. code-block:: yaml

   shape: 100


If the lights are in a matrix, then ``shape`` is a pair of numbers:
``[width, height]``.  For example, if you have a matrix that's 32 pixels wide
and 16 across, then you will write:

.. code-block:: yaml

   shape: [32, 16]


If the lights are in a cube, then ``shape`` is an ``[x, y, z]`` triple.
For example, if you have a cube that is 2 pixels wide, 4 pixels deep and 8
pixels high:

.. code-block:: yaml

   shape: [2, 4, 8]


The ``layout`` section
========================

The ``shape`` section is good enough for a lot of simple layouts but
more complex layouts to be specified will need the ``layout`` section.

We have the following layout classes:

## TODO-API

* ``strip``
* ``matrix``
* ``cube``
* ``circle``

----

.. bp-code-block:: footer

   shape: [32, 32]
   animation: $bpa.matrix.SpinningTriangle
