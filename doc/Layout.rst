class ``bibliopixel.layout.Layout``
===================================

``Layout`` provides the framework on which the [[Strip]] and [[Matrix]]
classes build. It cannot be used directly by itself. This is here to
document the methods it provides for the classes built upon it and for
anyone wanting to build upon it directly.

``__init__(drivers, threadedUpdate, brightness)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  ``drivers`` - A driver class or list of driver classes that inherit
   from ``bibliopixel.drivers.driver_base.[[DriverBase]]``. See the
   [[Drivers]] page for more info.
-  ``threadedUpdate`` - Display updates will run in background thread if
   True
-  ``brightness`` - Default master brightness value, 0-255

``_get_base(pixel)``
^^^^^^^^^^^^^^^^^^^^

-  ``pixel`` - Integer index of pixel in the buffer array.

Returns RGB tuple, (r,g,b), if pixel is in bounds. Otherwise returns
(0,0,0).

Not intended to be used directly. Provides basis for [[Strip]] and
[[Matrix]] calls.

``_set_base(pixel, color)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  ``pixel`` - Integer index of pixel in the buffer array.
-  ``color`` - RGB tuple, (r,g,b), representing the color to set.

Not intended to be used directly. Provides basis for [[Strip]] and
[[Matrix]] calls.

``waitForUpdate``
^^^^^^^^^^^^^^^^^

For use with ``threadedUpdate``. Calling will block until the current
update is complete. Intended for use when closing a script to allow the
current update to complete.

``update()``
^^^^^^^^^^^^

Pushes the current pixel buffer to the loaded driver. Callable from
[[Strip]] and [[Matrix]].

``setBuffer(buf)``
^^^^^^^^^^^^^^^^^^

-  ``buf`` - Pre-generated display buffer that must be in the format
   [R0, G0, B0, R1, G1, B1, ...] and contain *exactly*
   `bufByteCount <#bufbytecount>`__ (`numLEDs\*3 <#numleds>`__) number
   of values.

*Use Caution!* - ``setBuffer`` is provided for speed but bypasses
rotation, brightness, and color channel (depending on the driver)
control. It will raise ValueError if the buffer length is not the
required size.

``set_brightness(bright)``
^^^^^^^^^^^^^^^^^^^^^^^^^^

-  ``bright`` - An 8-bit (0-255) integer value to scale the brightness
   by.

Callable from [[Strip]] and [[Matrix]]. This will attempt to pass the
brightness setting to the loaded driver. Returns True if the driver
supports brightness directly, otherwise returns False. In many cases,
sending the brightness to the driver can be preferred. For example, some
driver chipsets support power levels directly, allowing a brightness to
be set without losing fidelity of the color value. For example, if the
brightness value is set to 128 and the driver does not support it, all
color values are simply scaled by 50%, also cutting the number of
possible colors by 50%. Chipsets that support direct power management
have the ability to decrease brightness while maintaining the full
color-space. In some instances, passing the brightness to the driver can
provide faster scaling operations, if supported by the driving device.

``setRGB(pixel, r, g, b)``
^^^^^^^^^^^^^^^^^^^^^^^^^^

-  ``pixel`` - Integer index of pixel in the buffer array.
-  ``r`` - 8-bit (0-255) Red color component.
-  ``g`` - 8-bit (0-255) Green color component.
-  ``b`` - 8-bit (0-255) Blue color component.

Callable from [[Strip]] and [[Matrix]]. Convenience method for setting
color with individual components instead of RGB tuple.

``setHSV(pixel, hsv)``
^^^^^^^^^^^^^^^^^^^^^^

-  ``pixel`` - Integer index of pixel in the buffer array.
-  ``hsv`` - 8-bit HSV tuple (h,s,v)

Callable from [[Strip]] and [[Matrix]]. Convenience method for setting
color with an 8-bit [[HSV\|HSV Colors]] tuple value.

``setOff(pixel)``
^^^^^^^^^^^^^^^^^

-  ``pixel`` - Integer index of pixel in the buffer array.

Callable from [[Strip]] and [[Matrix]]. Convenience method for setting
pixel to off.

``all_off()``
^^^^^^^^^^^^^

Callable from [[Strip]] and [[Matrix]]. High performance convenience
method for clearing the entire buffer.

Properties
~~~~~~~~~~

--------------

``driver``
^^^^^^^^^^

Callable from [[Strip]] and [[Matrix]]. The currently loaded driver
instance.

``numLEDs``
^^^^^^^^^^^

Callable from [[Strip]] and [[Matrix]]. Total number of LEDs based on
values provided by the driver.

``bufByteCount``
^^^^^^^^^^^^^^^^

Callable from [[Strip]] and [[Matrix]]. Total byte count in the display
buffer. Currently this is always `numLEDs <#numleds>`__ \* 3.

``lastIndex``
^^^^^^^^^^^^^

Callable from [[Strip]] and [[Matrix]]. The last valid pixel index
accepted by methods like `\_set\_base <#_set_basepixel-color>`__

``buffer``
^^^^^^^^^^

Callable from [[Strip]] and [[Matrix]]. The current display buffer, in
the format [R0, G0, B0, R1, G1, B1, ...]. \*Use caution. It is not
recommended to modify this directly. Use `setBuffer <#setbufferbuf>`__
instead.

``_set_brightness``
^^^^^^^^^^^^^^^^^^^

Callable from [[Strip]] and [[Matrix]]. The currently set 8-bit master
brightness value. If
`setMasterBrightness <#setmasterbrightnessbright>`__ returned True and
the driver took over brightness control, this will always be 255.
