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


Fields in a Palette
====================================

There are quite a few Fields below.  They're all optional but you can
experiment with them and not break anything, and you can get interesting
results that way.

You can also attach Palette Fields to a Control (described later in this
Tutorial) and change the values in real-time from an external source for
more excitement.

``colors`` (default ``[Black]``)
  A list of colors, or a string of color names separated with commas.
  Each color can be a string name, a hex string like #FFFFFF or 0xE8E0E8,
  or a triplet of integers like [255, 0, 255].  ``colors`` can also be the name
  of a Built-in or User Palette, in which case its Fields are copied and then
  possibly overwritten by Fields in this Palette.

``continuous`` (default ``False``)
  If ``True``, interpolate linearly between colors; otherwise
  use the nearest color from the original list.

``serpentine``
  If ``True``, palette colors are used in reverse order every
  other iteration, giving a back-and-forth effect.  Otherwise,
  palette colors always restart on each iteration

``scale``
  Scales the incoming index ``i``.  As ``i`` moves from 0
  to ``len(colors) - 1``, the whole palette repeats itself
  ``self.scale`` times

``offset``
  Offset added to the incoming index ``i``.  The offset is applied after scaling

``autoscale``
  If True, automatically rescale the Palette size to match the length of the
  output length. ``autoscale`` happens before ``scale``, so the two work well
  together to give banding or striping effects across your display

----

.. code-block:: yaml

   shape: [64, 48]
   animation:
     typename: $bpa.matrix.MathFunc
     func: 10
     palette: pastel

.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/palettes-footer.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/palettes-footer.gif
   :alt: Result
