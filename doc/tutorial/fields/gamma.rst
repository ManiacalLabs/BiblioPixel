``gamma``
------------------------------

This is an advanced topic and may be skipped on first reading.

The ``gamma`` Field corrects colors in the output display to account for how the
human eye sees.
`Here's
<https://www.siggraph.org/education/materials/HyperGraph/color/gamma_correction/gamma_intro.html>`_
a longer explanation.

Usually the correct gamma value will be automatically selected for you in
BiblioPixel based on your output hardware, but you might want to change this to
calibrate your display, to account for variations in manufacturing, or simply
for artistic reasons.

When a Driver has a ``gamma`` Field, you can leave it blank to let BiblioPixel
fill it in, or you can fill it yourself one of the following ways:

+ a single number ``gamma``
+ a list of three numbers - ``[gamma, offset, lower_bound]``
+ a dictionary with keys from ``gamma``, ``offset``, ``lower_bound``

Field definitions:

``gamma`` (default: depends on driver or ``1.0`` if no driver gamma)
   The gamma coefficient

``offset`` (default: ``0``)
   A small offset added after gamma correction to help cover the entire dynamic
   range

``lower_bound``
   The lowest output value for an LED component.  This is needed
   because some LED only emit light at values from 127-255.

.. bp-code-block:: footer

   shape: [64, 11]
   animation:
     typename: $bpa.strip.Rainbows.Rainbow
     palette: energy
