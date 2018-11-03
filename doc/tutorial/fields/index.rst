Field Types
------------------------------

BiblioPixel has many different types of Fields, and most of them are simple
things like strings or integers.

A few Fields do more interesting things like load Python code or make color
palettes and they are described in this section.

You can skim this on first reading.

.. toctree::
   :maxdepth: 1

   typenames
   types-of-typenames
   type-guessing
   palettes
   named-palettes
   fields-of-a-palette
   ledtype
   c_order
   gamma


.. bp-code-block:: footer

   shape: [64, 7]
   animation:
     typename: $bpa.matrix.Text.ScrollText
     text: 'The BiblioPixel Tutorial'
