class *bibliopixel.drivers.SimPixel.SimPixel*
=============================================

This class sends information to a WebGL program running locally in a
browser page. You can see it run by loading the web page at
http://simpixel.io/.

``__init__(num, port=1337, layout=None)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  **``num``** - Number of pixels to be displayed.
-  **``port``** - Optional: the port number to use. 1337 is the default
   used on http://simpixel.io/
-  **``pixel_positions``** - Optional: A flat list of [x,y,z] (integer)
   coordinates for each pixel in the display. The [[Layout]] used will
   automatically generate and pass in this value but you can override it
   by providing a value here. Using the pixel\_positions\_from\_\*
   methods in bibliopixel.layout.geometry is the easiest way to generate
   this value.
