The whole point of BiblioPixel is to display varied colors so there are,
of course, a multitude of methods to manipulate color data, all
contained in [[bibliopixel.colors\|Colors-Module]].

In BiblioPixel, colors are stored as a tuple of three 1-byte colors
values: ``(R,G,B)`` Each value in the tuple can range from 0 (off) to
255 (full brightness) for that color channel. Below are some examples of
methods that can be used to modify these color values.

Note, all examples below assume you have imported the [[colors
module\|Colors-Module]] as follows:

.. code:: python

    import bibliopixel.colors as colors

Color Scaling
~~~~~~~~~~~~~

Scaling is simply the process of changing the brightness by a
percentage. You can only decrease the color brightness:

.. code:: python

    a = (255,255,255) #pure white
    b = colors.color_scale(a, 128) #scale by 50% (128 is half of 255)
    #b now equals (128,128,128) - a light gray

Color Blending
~~~~~~~~~~~~~~

Sometimes you may want to mix two colors together, this can be done via
color\_blend:

.. code:: python

    purple = colors.color_blend((255,64,0), (0,32,255))
