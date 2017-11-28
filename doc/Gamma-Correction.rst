Many of the [[drivers\|DriverBase]] support an optional *gamma*
parameter that allows for providing a `gamma
correction <http://en.wikipedia.org/wiki/Gamma_correction>`__ table to
be applied to all colors values. This table represents a pre-generated
gamma curve instead of providing the function curve for the sake of
performance.

Many LED strips do not provide LEDs where each channel has a direct
linear relation to one another, causing the colors to not always look
correct. The gamma correction attempts to fix this.

The module bibliopixel.gamma contains some pre-generated gamma tables
that make an attempt at providing a best average gamma curve for
specific chipsets. But the specific curve needed can change depending on
a wide variety of factors. It may not be needed, however, so try it
without and see how it looks first.

The curve table ***must*** provide a list of exactly 256 integer values.
For example, the gamma table for the WS2801 chipset is defined as:

.. code:: python

    WS2801 = [int(pow(float(i) / 255.0, 2.5) * 255.0) for i in range(256)]
    # or, easier with bibliopixel.gamma.Gamma()
    WS2801 = Gamma(gamma=2.5)

To use these gamma corrections with a driver that supports them, simple
load the correction table into the driver as follows:

.. code:: python

    #from bibliopixel.gamma
    driver = Serial(type = LEDTYPE.WS2801, num = 12, gamma = bibliopixel.gamma.WS2801)
    #manual entry
    driver = Serial(type = LEDTYPE.WS2801, num = 12, gamma = [int(pow(float(i) / 255.0, 2.5) * 255.0) for i in range(256)])

Currently provided values in bibliopixel.gamma are: APA102, LPD8806,
WS2801, SM16716, LPD6803, WS2812B, WS2812, NEOPIXEL, DEFAULT (no
correction).

The [[LPD8806]] and [[WS2801]] classes automatically apply the correct
gamma correction.
