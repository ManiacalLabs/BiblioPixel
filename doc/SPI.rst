class *bibliopixel.drivers.SPI.SPI*
===================================

SPI() is for controlling anything that can utilize the SPI interface
available on devices like the Raspberry Pi. See [[SPI Setup]] for more
details on connecting SPI hardware.

**Note:** SPI devices typically require root access in order to write to
the SPI port. Any scripts using this class should be run with *sudo*.

Unlike the SPI drivers in BiblioPixel 2, there is a single SPI driver
for all LED types.

``__init__(ledtype, num, dev='/dev/spidev0.0', interface='FILE', spi_speed=1, c_order = ChannelOrder.RGB, gamma=gamma.DEFAULT)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  **ledtype** - Type of LEDs connected. See `LED
   Types <Serial#led-types>`__.
-  **num** - Number of pixels to be controlled.
-  **dev** - The SPI device path to use. See [[SPI Setup]] for more
   details.
-  **interface** - SPI interface handler to use. See `SPI
   Interfaces <#spi-interfaces>`__ below for more details.
-  **spi\_speed** - The SPI speed, in MHz, to use when communicating
   with the strip. WS2801 requires 1Mhz and WS2812X requires 3.2MHz, do
   not change for these types.
-  **c\_order** - Optional: Channel order used by the attached display.
   Can be any of the six options in the ChannelOrder class. See
   [[Channel Order\|Display-Setup#channel-order]] for more details.
-  **gamma** - Optional: Set [[Gamma Correction]] for the output. The
   correct default gamma will automatically be chosen for each LED type
   if this value is not passed. Only use to override.

SPI interfaces
~~~~~~~~~~~~~~

There are three different ways that BiblioPixel can communicate with
SPI.

-  **FILE** - This is the default interface: it accesses the SPI port as
   a Unix-style file. This mechanism requires no external dependencies,
   so it's suitable for any machine - but you cannot set the SPI speed,
   and you cannot control WS281X at all strips as a result.

-  **PERIPHERY** - Uses the
   `python-periphery <https://github.com/vsergeev/python-periphery>`__
   pure python library to access the SPI port via low level system
   calls. This interface has greater support for non-Pi devices like the
   BeagleBone or Orange Pi.

-  **PYDEV** - Uses the
   `python-spidev <https://pypi.python.org/pypi/spidev>`__ library to
   access the SPI port. This is the official Raspberry Pi driver but is
   now old and not recommended unless you can't use any of the others.

Notes
~~~~~

-  All three interfaces drivers use the same mechanism under the hood to
   speak to SPI: a Unix-style file handle at /dev/spidevX.Y.
-  WS281X: WS281X only works with PERIPHERY and PYDEV and is limited to
   455 pixels max. If you need more pixels than that and are using a
   Raspberry Pi, use the [[PiWS281X]] driver. Otherwise, we recommend
   the `AllPixel <http://maniacallabs.com/AllPixel>`__.
-  WS2801 only works at 1MHz SPI speed.
