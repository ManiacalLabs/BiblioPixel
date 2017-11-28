class *bibliopixel.Circle*
==========================

Circle provides methods to control pixels arranged in concentric
circles. It inherits from [[LEDBase]] and provides all of its public
methods and properties. Circle actually lives at bibliopixel.led.Strip
but can be accessed at bibiliopixel.Circle for convenience.

Unlike [[Strip]] or [[Matrix]], the pixels on a circular display are
*not* accessed by index or (x,y) coordinate. Instead, a `polar
coordinate <http://en.wikipedia.org/wiki/Polar_coordinate_system>`__
system is used. While it may seem odd at first, it's much easy to
specify the pixels by:

-  Ring: Index of the concentric ring on the circle. The center point
   (or smallest ring) is index 0 and the indices count up from there to
   the outer-most ring.

-  Angle: 0-359 value of the angle on the circle. Negative values are
   allowed.

Currently, the only known commercial LED display that is arranged like
this is one `sold by
Adafruit <https://www.adafruit.com/products/2477>`__. As you can see in
the
`datasheet <https://www.adafruit.com/images/product-files/2477/2477.pdf>`__,
the LEDs are, in fact, arranged in concentric circles and not a spiral.
This code will *not* work with a spiral as you must specify the number
of pixels in each ring.

One other use for this, for example, would be on a Christmas tree
display. As long as care is taken to arrange the pixels in parallel
rings, increasing in size down the tree, it should work quite nicely.

\_\_init\_\_
^^^^^^^^^^^^

(driver, rings, rotation, maxAngleDiff=0, threadedUpdate=False,
brightness=255)

-  **driver** - A driver class or list of driver classes that inherit
   from bibliopixel.drivers.driver\_base.[[DriverBase]]. See the
   [[Drivers]] page for more info.
-  **rings** - Array of first and last pixel index in each ring. For
   example, the ring mapping for the Adafruit display mentioned above
   is:

   .. code:: python

       rings = [
       [254,254],  #0 - Center point
       [248,253],  #1
       [236,247],  #2
       [216,235],  #3
       [192,215],  #4
       [164,191],  #5
       [132,163],  #6
       [92,131],   #7
       [48,91],    #8
       [0,47],     #9 - Outer most ring
       ]

-  **maxAngleDiff** - Maximum angle the resolved pixel can be from the
   given angle. If outside of that range (in either direction) the pixel
   will be dropped. Setting to 0 (default) means to limit.
-  **rotation** - Degrees (-359 through 359) to rotate entire display
   by.
-  **threadedUpdate** - Display updates will run in background thread if
   True. Defaults to False.
-  **masterBrightness** - Default master brightness value, 0-255

angleToPixel
^^^^^^^^^^^^

(angle, ring)

-  **angle** - Angle (0-359) of pixel on the circle. Nearest pixel to
   that angle, rounded down, will be chosen.
-  **ring** - Index of the ring on which the pixel lies.

Returns pixel index of nearest pixel to (angle, ring). Should not
generally be used.

set
^^^

(ring, angle, color)

-  **ring** - Index of the ring on which the pixel lies.
-  **angle** - Angle (0-359) of pixel on the circle. Nearest pixel to
   that angle, rounded down, will be chosen.
-  **color** - RGB tuple, (r,g,b), representing the color to set.

Set value of pixel at (angle, ring) to given color.

get
^^^

(ring, angle)

-  **ring** - Index of the ring on which the pixel lies.
-  **angle** - Angle (0-359) of pixel on the circle. Nearest pixel to
   that angle, rounded down, will be chosen.

Returns RGB tuple, (r,g,b), if pixel is in bounds. Otherwise returns
(0,0,0).

drawRadius
^^^^^^^^^^

(angle, color, startRing, endRing)

-  **angle** - Angle (0-359) of pixel on the circle. Nearest pixel to
   that angle, rounded down, will be chosen.
-  **color** - RGB tuple, (r,g,b), representing the color to draw.
-  **startRing** - Index of the ring where the line should start.
-  **endRing** - Index of the ring where the line should stop. Defaults
   to [[lastRing\|Circle#lastring]].

Draws a line along a given angle from startRing to endRing, in the given
color

fillRing
^^^^^^^^

(ring, color, startAngle, endAngle)

-  **ring** - Index of ring to fill.
-  **color** - RGB tuple, (r,g,b), representing the color to fill.
-  **startAngle** - Angle where the fill should start.
-  **endAngle** - Angle where the fill should stop. Defaults to 359.

Fills (draws and arc) along a given ring with the given color.

Properties
~~~~~~~~~~

--------------

rings
^^^^^

Array of the ring mapping provided init method.

ringCount
^^^^^^^^^

Total number of rings.

lastRing
^^^^^^^^

Index of the outer most ring on the circle.

ringSteps
^^^^^^^^^

Array of degrees between each pixel for the given ring index.
