Fields of a Palette
-------------------------

Palettes have several extra fields for special effects.  They're all optional
but you can experiment with them and not break anything, and you can get
interesting results that way.

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

.. bp-code-block:: footer

   shape: [64, 48]
   animation:
     typename: $bpa.strip.Pulse
     colors: ['lime', 'dark olive green', 'emerald green']
