class \_bibliopixel.drivers.spi\_driver\_base.DriverSPIBase
===========================================================

DriverSPIBase is a base class for building other drivers that control
SPI strips on devices that have hardware SPI ports, like the Raspberry
Pi or BeagleBone Black. [[DriverLPD8806]] and [[DriverWS2801]] both
inherit from this class. See [[SPI Setup]] for more details on using
hardware SPI.

**Note:** SPI devices typically require root access in order to write to
the SPI port. Any scripts using this class should be run with *sudo*.

\_\_init\_\_
^^^^^^^^^^^^

(num, c\_order = ChannelOrder.GRB, use\_py\_spi = True,
dev="/dev/spidev0.0", SPISpeed = 16):

-  **num** - Number of pixels to be controlled.
-  **c\_order** - Optional: Channel order used by the attached display.
   Can be any of the six options in the ChannelOrder class. See
   [[Channel Order\|Display-Setup#channel-order]] for more details.
-  **use\_py\_spi** - If True, SPI communication is handled by
   `py-spidev <https://github.com/doceme/py-spidev>`__ which provides
   faster output. Otherwise a file access method is used.
-  **dev** - The SPI device path to use. See [[SPI Setup]] for more
   details.
-  **SPISpeed** - The SPI speed, in MHz, to use when communicating with
   the strip.

update
^^^^^^

(data)

-  **data** - Pixel data in the format [R0, G0, B0, R1, G1, B1, ...]

The default update() implementation for SPI. It will call
`\_fixData() <DriverBase#_fixdatadata>`__ and then send to pixel data to
the SPI device. Only override this method if a different implementation
is required.

\_sendData
^^^^^^^^^^

This method is called in the default update() method and sends the data
to the SPI port. If update() is overridden in an inheriting class, it
will need to be called manually.

Properties
~~~~~~~~~~

--------------

dev
^^^

The path of the hardware SPI device to be used. On the Raspberry Pi and
BeagleBone Black the default device path is /dev/spidev0.0

use\_spi\_spy
^^^^^^^^^^^^^

Holds True if `py-spidev <https://github.com/doceme/py-spidev>`__ is
being used for SPI communication, otherwise False.

\_spiSpeed
^^^^^^^^^^

Holds the currently set SPI speed.

spi
^^^

The connected SPI device object. A
`py-spidev <https://github.com/doceme/py-spidev>`__ if use\_py\_spi ==
True, otherwise a file handle to the SPI device. Generally, this
property need not be accessed as it is all handled in the update()
method.
