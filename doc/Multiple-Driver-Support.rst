As of v1.1.0, BiblioPixel supports multiple separate output drivers to
be used with a single [[Strip]] or [[Matrix]] instance. This allows
multiple displays to be treated as on single, larger display. For
example, the `AllPixel <http://maniacallabs.com/AllPixel>`__ can handle
a maximum of 700 pixels. Two AllPixel boards could be used, each driving
half of a 1400 pixel display. But in BiblioPixel, each pixel can be
addressed as if it were a single display with only one driver. See
`multi\_matrix\_demo.py <https://github.com/ManiacalLabs/BiblioPixel/blob/master/multi_matrix_demo.py>`__
for an example of how this can be used.

Note, however, that using multiple drivers as a single display with
[[Matrix]] requires some more advanced coordinate mapping that cannot be
handled automatically as it depends on the physical layout of the
display. See more details in the [[MultiMapBuilder and
mapGen\|Display-Setup#multimapbuilder-and-mapgen]] section.

To take advantage of this feature, each AllPixel needs to be assigned a
DeviceID. See the [[DeviceID\|Device-ID]] section for info on how to use
the DeviceIDManager script.

When using Strip, it's simple. If you have two lengths of LEDs, each
with 100 pixels, and each hooked up to their own driver, the second
strand would be addressed at an offset of 100, instead of starting back
at 0. For example:

.. code:: python

    from bibliopixel.layout import *
    from bibliopixel.drivers.serial import *
    import bibliopixel.colors as colors

    driverA = Serial(LEDTYPE.LPD8806, 100, deviceID = 1)
    driverB = Serial(LEDTYPE.LPD8806, 100, deviceID = 2)

    led = Strip(200, [driverA, driverB])

    for i in range(200):
       led.fill(colors.Red, 0, i)
       led.update()

The above example would fill up the strip one at a time, across both of
the 100 pixel sections. The index of the first pixel on the first
section is 0, but the index of the first pixel on the second section is
100, because the first section has 100 pixels.
