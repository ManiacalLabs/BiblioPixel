class *bibliopixel.drivers.image\_sequence.ImageSequence*
=========================================================

ImageSequence is a crude driver, designed primarily for the creation of
this documentation. It is in a "good enough" state now and will likely
be updated in the future if the need presents itself.

Its main purpose to to output each generated frame to an image file on
disk. If desired, the sequence of images can then be processed into an
animated GIF with a tool like ImageMagick. There is no preservation of
the timing between each frame since it, currently, does not output
directly to a GIF, only separate PNG files.

\_\_init\_\_
^^^^^^^^^^^^

(num = 0, width = 0, height = 0, pixelSize = 10)

-  **num** - Number of pixels to be displayed.
-  **width** - Optional: Width of display buffer. If using [[Matrix]],
   its width property will automatically be set from this value.
-  **height** - Optional: Height of display buffer. If using [[Matrix]],
   its height property will automatically be set from this value.
-  **pixelSize** - Width and height to render each pixel in the final
   image. Effectively a scale value for the image output.

writeSequence
^^^^^^^^^^^^^

(output, clear = True)

-  **output** - Directory to write image sequence to.
-  **clear** - True will cause the image sequence buffer to be cleared
   after writing out the sequence. Prevents previous frames from being
   written out on next call to this method.

Writes the current frame buffer out to images on disk. Images are named
0000.png, 0001.png, 0002.png, etc. This should be called after the
animation completes, so the animation must not run forever. After the
images have been written, the following `ImageMagick <>`__ command could
be used to generate an animated GIF:

.. code:: bash

    convert -delay 25 -loop 0 *.png animation.gif

This will create a GIF with a 250ms delay between each frame (-delay 25)
and loops forever (-loop 0).
