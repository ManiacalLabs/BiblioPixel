class *bibliopixel.drivers.dummy\_driver.Dummy*
===============================================

Dummy is provided mainly for testing. It allows the rest of the library
and animations to run without actually having to connect a display.
There is, however, no visual feedback. If testing without physical
hardware is needed, try [[SimPixel]].

\_\_init\_\_
^^^^^^^^^^^^

(num, delay = 0)

-  **num** - Number of pixels to be controlled.
-  **delay** - Artificial delay in milliseconds to simulate time to push
   pixel data to the display.
