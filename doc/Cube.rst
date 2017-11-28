class *bibliopixel.Cube*
========================

Cube provides methods to control a full 3D layout of pixels. It inherits
from [[Layout]] and provides all of its public methods and properties.

\_\_init\_\_
^^^^^^^^^^^^

(driver, x, y, z, coordMap = None, threadedUpdate = False,
brightness=255)

-  **driver** - A driver class or list of driver classes that inherit
   from bibliopixel.drivers.driver\_base.[[DriverBase]]. See the
   [[Drivers]] page for more info.
-  **x** - Required: x dimension of layout
-  **y** - Required: y dimension of layout
-  **z** - Required: z dimension of layout
-  **coordMap** - A basic, serpentine, 3D layout will be auto-generated
   if this is not provided. If you require more control use
   bibliopixel.layout.gen\_cube()
-  **threadedUpdate** - Display updates will run in background thread if
   True. Defaults to False.
-  **masterBrightness** - Default master brightness value, 0-255

set
^^^

(x, y, z, color)

-  **x** - x coordinate of pixel
-  **y** - y coordinate of pixel
-  **z** - z coordinate of pixel
-  **color** - RGB tuple, (r,g,b), representing the color to set.

Set value of pixel at (x,y, z) coordinate to given color or texture
color.

get
^^^

(x, y, z)

-  **x** - x coordinate of pixel
-  **y** - y coordinate of pixel
-  **z** - z coordinate of pixel

Returns RGB tuple, (r,g,b), if pixel is in bounds. Otherwise returns
(0,0,0).

setHSV
^^^^^^

(x, y, z, hsv)

-  **x** - x coordinate of pixel
-  **y** - y coordinate of pixel
-  **z** - z coordinate of pixel
-  **hsv** - 8-bit HSV tuple (h,s,v)

Convenience method for setting color with an 8-bit [[HSV]] tuple value.

setRGB
^^^^^^

(x, y, z, r, g, b)

-  **x** - x coordinate of pixel
-  **y** - y coordinate of pixel
-  **z** - z coordinate of pixel
-  **r** - 8-bit (0-255) Red color component.
-  **g** - 8-bit (0-255) Green color component.
-  **b** - 8-bit (0-255) Blue color component.

Convenience method for setting color with individual components instead
of RGB tuple.
