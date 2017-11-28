USB Serial devices like the
`AllPixel <http://maniacallabs.com/AllPixel/>`__ (which uses the
ATMega32u4) don't typically have unique serial numbers programmed into
the device. Because of this, there is no guarantee what COM port name
the device will be assigned when using multiple devices. Even if the
devices are left plugged in, a system reboot can completely re-assign
the port names, depending on the order in which the devices were
enumerated.

This was problematic when using multiple devices like the
`AllPixel <http://maniacallabs.com/AllPixel/>`__ with BiblioPixel's
[[Multiple Driver Support]]. Each serial device connects to a specific
region of a display so BiblioPixel, therefore, must know which port name
corresponds to which device without having to reconfigure the drivers
after each system boot. This is where device IDs come in.

[[Serial]] now includes an optional parameter that allows specifying a
unique 8-bit device ID, making it possible to differentiate between 256
different devices. But first, the IDs must be set. To do so, check out
the instructions for the [[Serial Device Commands]].

Once you have set the device IDs, simply provide it to [[Serial]] in the
init parameters:

.. code:: python

    driver0 = Serial(LEDTYPE.NEOPIXEL, 100, device_id = 0)
    driver1 = Serial(LEDTYPE.NEOPIXEL, 100, device_id = 1)
    driver2 = Serial(LEDTYPE.NEOPIXEL, 100, device_id = 2)
