Project Sections
-------------------

A quick description of each section
=============================================

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

``palettes``
    A dictionary of named *Palettes*.  A Palette is a list of colors, together
    with instructions on how to lay them out and interpolate between them.

``run``
    Controls how the topmost Animation is executed - how fast it runs, for how
    long or for how many times, and more.

``shape``
    The shape of the layout - ``length`` for strips, ``[width, height]`` for
    matrices and ``[x, y, z]`` for cubes.

.. bp-code-block:: footer

   shape: [64, 8]
   animation: $bpa.strip.ColorPattern
