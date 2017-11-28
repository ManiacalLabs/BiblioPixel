class *bibliopixel.drivers.hue.Hue*
===================================

Hue is for controlling devices in the `Philips
Hue <http://www2.meethue.com/en-us/>`__ product line. It requires the
`phue <https://github.com/studioimaginaire/phue>`__ python package which
can be installed by running "pip install phue". The utility of this
driver is fairly limited compared to most as the Hue lights were not
designed to be updated quickly. High frame-rate animations are just
about impossible, but Hue is still useful for those that want to
directly program their lights.

\_\_init\_\_
^^^^^^^^^^^^

(num, ip, nameMap = None):

-  **num** - Number of pixels to be controlled.
-  **ip** - IP address of the Hue bridge. See `this
   tutorial <https://github.com/sqmk/Phue/wiki/Finding-Philips-Hue-bridge-on-network>`__
   for more on how to find the IP.
-  **nameMap** - An optional list of names that correspond to the set
   names of each light device. Useful for setting the order of the
   lights within the "display". By default, Hue uses whatever order is
   returned from the Hue bridge.

setTransitionTime
^^^^^^^^^^^^^^^^^

(time):

-  **time** - Float value representing the number of seconds over which
   to transition from one color to the next when setting a device's
   color.

Hue defaults to a transition time of 0, where all changes happen
instantly. By setting this to a greater value, the lights will take care
of automatically fading from one color to the next.
