The ``ledtype`` Field identifies the type of LED strip
---------------------------------------------------------

Each type of LED strip has different characteristics. The ``ledtype`` field is a
string in the ``Driver`` section of the ``Serial`` driver which identifies which
type of strips are being used.

The ``ledtype``\ s are:

+ APA102, SK9822
+ LPD1886
+ LPD8806
+ P9813
+ SM16716
+ TM1803
+ TM1804, TM1809
+ UCS1903
+ WS2801
+ APA104, NEOPIXEL, WS2811, WS2812, WS2812B
+ WS2811_400
+ GENERIC  # means "no processing"

If you don't see your brand of LED strip, just ask the `mailing list
<https://groups.google.com/d/forum/maniacal-labs-users>`_. It's very likely
that it's either a variant of one of the above, or we can quickly figure out how
to handle it.

.. bp-code-block:: footer

   shape: [64, 11]
   animation:
     typename: $bpa.strip.Rainbows.Rainbow
     palette: energy
