The ``c_order`` Field
-----------------------------

The ``c_order`` Field identifies the order of colors on an LED strip.

The order of the color RGB components in LED strips is unfortunately different
between different brands, even with the same part number or from the same
manufacturer.

The ``c_order`` Field can have these values:

+ RGB
+ RBG
+ GRB
+ GBR
+ BRG
+ BGR

The field is case-insensitive, so you can enter values like ``grb``.  It also
accepts any integer, which selects an order from the ``c_order`` list, wrapping
around in both directions.

.. bp-code-block:: footer

   shape: [64, 11]
   animation:
     typename: $bpa.strip.Rainbows.Rainbow
     palette: bold
