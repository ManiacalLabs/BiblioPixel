Configuring Your AllPixel or Serial Device
==========================================

If you are using an `AllPixel <http://maniacallabs.com/AllPixel>`__ or
other serial device which implements a compatible firmware, you can use
the BiblioPixel ``devices`` and ``all_pixel`` commands to configure your
device.

Both commands below optionally take the following arguments. These are
never required for an official AllPixel.

-  ``--hardware-id``: Vendor and Product ID pair of the USB Serial
   device, such as ``1D50:60AB``
-  ``--baud``: Serial baud rate to connect to the device at.

``devices`` Command
-------------------

This command will allow you to set the device ID on your device. Doing
so allows you to later run multiple devices simultaneously and have
BiblioPixel differentiate between them.

Run this command as follows:

``bibliopixel devices``

You will be greeted with the following process:

::

    Press Ctrl+C any time to exit.

    Connect just one Serial device (AllPixel) and press enter...
    Device ID of /dev/ttyACM0: 0
    Input new ID (enter to skip): 42
    Device ID set to: 42

    Connect just one Serial device (AllPixel) and press enter...

As seen above, it will display the current device ID of the connected
device and then let you enter a new ID. It will continue looping this
process until you Ctrl+C to exit out.

``all_pixel`` Command
---------------------

This command will walk you through the setup options for your AllPixel
compatible device. The main intent for the usage of this command is if
you needed to configure a device for use with software other than
BiblioPixel.

Run this command as follows:

``bibliopixel all_pixel``

Once run and as long as you have a single AllPixel compatible device
connected, you will be greeting with the following process:

::

    Press Ctrl+C anytime to quit.

    Scanning for devices...

    Choose LED Type
     0: GENERIC
     1: LPD8806
     2: WS2801 
     3: WS2812/NEOPIXEL
     4: APA104
     5: WS2811_400
     6: TM1809/TM1804
     7: TM1803 
     8: UCS1903
     9: SM16716
    10: APA102/DOTSTAR
    11: LPD1886
    12: P9813

    Choice: 1

    Number of LEDs: 120

    SPI Speed (1-24): 12

    Device: ('/dev/ttyACM0', 0)
    LED Type: LPD8806
    Num LEDs: 120
    SPI Speed: 12
