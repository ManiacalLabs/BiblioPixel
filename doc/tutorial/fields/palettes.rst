Palettes
------------

Animations can have a ``palette`` Field that describes the colors they use.

A Palette is a list of colors, together with other optional Fields with
entertaining names like ``serpentine`` that change how these colors are used to
paint pixels.

All Animations already have a ``palette`` Field, though not all of them actually
do anything with it - most of the animations in BiblioPixelAnimations do.

**Example 1**: Three ways of writing the same palette

.. code-block:: yaml

    palette: 'red, green, blue'  # A string

    palette: [red, green, blue]  # A list of strings

    palette:  # A dictionary where "colors" has a list of strings
      colors:
        - red
        - green
        - blue


**Example 2**: A more complex Palette

.. code-block:: yaml

    # Describes a palette that starts at red, smoothly moves to blue,
    # then to green, then reverses, smoothly moves back to blue, then to red,
    # then repeats.
    palette:
      colors: [red, green, blue]
      continuous: True
      serpentine: True


.. bp-code-block:: footer

   shape: [64, 48]
   animation:
     typename: $bpa.matrix.MathFunc
     func: 10
     palette:
       colors: pastel
       scale: 0.01
