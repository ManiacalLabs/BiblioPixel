class *bibliopixel.drivers.driver\_base.DriverBase*
===================================================

DriverBase provides the framework on which driver classes build. It
cannot be used directly by itself. This is here to document the methods
it provides for the classes built upon it and for anyone wanting to
build their own drivers.

\_\_init\_\_
^^^^^^^^^^^^

(num, width = 0, height = 0, c\_order = ChannelOrder.RGB, gamma = None)

-  **num** - Number of pixels to be controlled.
-  **width** - Optional: Width of matrix display. If using [[Matrix]],
   its width property will automatically be set from this value.
-  **height** - Optional: Height of matrix display. If using [[Matrix]],
   its height property will automatically be set from this value.
-  **c\_order** - Optional: Channel order used by the attached display.
   Can be any of the six options in the ChannelOrder class. See
   [[Channel Order\|Display-Setup#channel-order]] for more details.
-  **gamma** - 256 value gamma correction list. The list *MUST* contain
   256 8-bit integer values. Predefined corrections lists can be found
   in [[bibliopixel.gamma\|Gamma-Correction]]

For new drivers that inherit from DriverBase, only the num parameter
needs to be made available, but it is greatly suggested that the rest
are also made available to provide a common interface.

update
^^^^^^

(data)

-  **data** - Pixel data in the format [R0, G0, B0, R1, G1, B1, ...]

The driver update() method is automatically called by the update()
method of [[Strip]] or [[Matrix]]. This method *MUST* be implemented by
new driver classes and is where the pixel data should be pushed to the
display.

setMasterBrightness
^^^^^^^^^^^^^^^^^^^

(brightness)

-  **brightness** - 8-bit (0-255) brightness value.

This method only need be implemented by new drivers if it is for a
device that supports brightness control in hardware. If it is
implemented, the method must return true to inform [[Strip]] or
[[Matrix]] that brightness control has been passed off to the driver.
When `setMasterBrightness <DriverBase#setmasterbrightnessbright>`__ is
called on [[Strip]] or [[Matrix]], it will first check if the driver
supports it and, if not, will fall back to scaling colors internally.

\_fixData
^^^^^^^^^

(data)

-  **data** - Pixel data in the format [R0, G0, B0, R1, G1, B1, ...]

This method should be called byte the driver's update() method. The
default implementation in DriverBase will re-order the color channels
and apply gamma correction if available. In most cases this is good
enough, but the method may be overridden if anything extra is needed. If
this method is not called in a new driver's update() method, the
c\_order and gamma options should not be made available in that driver's
**init**.

Properties
~~~~~~~~~~

--------------

numLEDs
^^^^^^^

Number of LEDs to be controlled by the driver.

gamma
^^^^^

256 value gamma correction list. Predefined corrections lists can be
found in [[bibliopixel.gamma\|Gamma-Correction]].

c\_order
^^^^^^^^

Currently set channel order being used by the driver.

width
^^^^^

Width of the matrix controlled by the driver, if set.

height
^^^^^^

Height of the matrix controlled by the driver, if set.

bufByteCount
^^^^^^^^^^^^

Expected total byte count in the display buffer. Currently this is
always `numLEDs <#numleds>`__ \* 3.

\_buf
^^^^^

Where the channel and gamma corrected data is placed by
`\_fixData <#_fixdatadata>`__ and what should then be used by
`update() <#update>`__ to push to the display. This data buffer is used
because some drivers, like [[LPD8806]] require extra data bytes before
or after the pixel data and this allows `\_fixData <#_fixdatadata>`__ to
just manipulate the pixel data.
