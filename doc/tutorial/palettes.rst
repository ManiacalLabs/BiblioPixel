Palettes
------------

Animations can have a ``"palette"`` Field that describes the colors they use.

Many BiblioPixel Animations already have a ``"palette"`` Field and we will be
adding this new feature to more of them over time.  You can also use Palettes in
your own Animations immediately.

A Palette is a list of colors, together with other optional Fields with
entertaining names like "serpentine" that change how these colors are used to
paint pixels.

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


Named Palettes
=================

You can use a named Palette anywhere you need a palette.

There are twenty named Built-In Palettes that come with BiblioPixel and you can
also define your own named Project Palettes on a per-project basis, or re-use a
named Palettes between Projects.

The list of Built-In Palettes is in the source code
`here
<https://github.com/ManiacalLabs/BiblioPixel/blob/master/bibliopixel/util/colors/palettes.py#L34-L56>`_ .


**Example 3**: Project Palettes and Built-in Palettes

.. code-block:: yaml

    palettes:
       hideous: [yellow, beige, maroon]

    animation:
      typename: sequence
      length: 5
      animations:
        - typename: $bpa.matrix.MathFunc
          palette: hideous  # Project Palette

        - typename: $bpa.matrix.MathFunc
          palette: flag     # Built-In Palette

.. bp-code-block:: footer

   shape: [64, 48]
   animation:
     typename: $bpa.matrix.MathFunc
     func: 10
     palette:
       colors: pastel
       scale: 0.01
