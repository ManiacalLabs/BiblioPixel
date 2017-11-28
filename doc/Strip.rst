class *bibliopixel.Strip*
=========================

Strip provides methods to control a single, 1-dimensional LED strip. It
inherits from [[Layout]] and provides all of its public methods and
properties. Strip actually lives at bibliopixel.layout.Strip but can be
accessed at bibiliopixel.Strip for convenience.

\_\_init\_\_
^^^^^^^^^^^^

(driver, threadedUpdate=False, brightness=255, pixelWidth=1)

-  **driver** - A driver class or list of driver classes that inherit
   from bibliopixel.drivers.driver\_base.[[DriverBase]]. See the
   [[Drivers]] page for more info.
-  **threadedUpdate** - Display updates will run in background thread if
   True. Defaults to False.
-  **brightness** - Default master brightness value, 0-255
-  **pixelWidth** - Sets pixel size scaling. Setting to > 1 will make
   each "logical" pixel *pixelWidth* LEDs wide and appropriately scale
   numLEDs to match. For example, pixelWidth=5 means that each call to
   set() will set that color to a group of 5 pixels.

set
^^^

(pixel, color)

-  **pixel** - Integer index of pixel in the buffer array. If
   pixelWidth, from above, is > 1, this is a "logical" pixel index.
-  **color** - RGB tuple, (r,g,b), representing the color to set.

Set value of pixel to given color.

get
^^^

(pixel)

-  **pixel** - Integer index of pixel in the buffer array.

Returns RGB tuple, (r,g,b), if pixel is in bounds. Otherwise returns
(0,0,0).

fill
^^^^

(color, start=0, end=-1)

-  **color** - RGB tuple, (r,g,b), representing the color to fill.
-  **start** - Index of the pixel where the fill should start.
-  **end** - Index of the pixel where the fill should stop. Defaults to
   [[lastIndex\|LEDBase#lastindex]].

Sets all pixels to given color from start index to end index. By default
sets every pixel on the strip.

fillRGB
^^^^^^^

(r, g, b, start=0, end=-1)

-  **r** - 8-bit (0-255) Red color component.
-  **g** - 8-bit (0-255) Green color component.
-  **b** - 8-bit (0-255) Blue color component.
-  **start** - Index of the pixel where the fill should start.
-  **end** - Index of the pixel where the fill should stop. Defaults to
   [[lastIndex\|LEDBase#lastindex]].

Convenience method for setting color with individual components instead
of RGB tuple. By default, fill() sets the given color to every pixel on
the strip.

fillHSV
^^^^^^^

(hsv, start=0, end=-1)

-  **hsv** - 8-bit HSV tuple (h,s,v)
-  **start** - Index of the pixel where the fill should start.
-  **end** - Index of the pixel where the fill should stop. Defaults to
   [[lastIndex\|LEDBase#lastindex]].

Convenience method for setting color with an 8-bit HSV tuple value (see
[[HSV Colors]]). By default, fill() sets the given color to every pixel
on the strip.
