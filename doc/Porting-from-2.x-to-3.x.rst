Porting from 2.x to 3.x
=======================

As much as possible we've tried to make BiblioPixel 3.0 as backwards
compatible as possible with 2.x, so in many cases your code should just
work. But there are a few things to be aware of as you get started.

Now Python 3.x only!
^^^^^^^^^^^^^^^^^^^^

By far, the biggest change is that we have completely dropped Python 2
support. Inst ing BiblioPixel via pip will now fail on Python 2 unless
you use ``pip install BiblioPixel<=3`` to force it to install the older
version. We support Python 3.4, 3.5, and 3.6. As with any work with
python, but especially with Python 3, we highly recommend installing
everything inside a
`virtualenv <https://virtualenv.pypa.io/en/stable/>`__.

Base LED handlers
^^^^^^^^^^^^^^^^^

In BiblioPixel 2.x you could choose from ``LEDStrip``, ``LEDMatrix``,
``LEDPOV``, and ``LEDCircle``. In BiblioPixel 3.0 we've dropped the
``LED`` part and you can import the following from ``bibliopixel.led``:

-  ``Strip``
-  ``Matrix``
-  ``Cube``
-  ``Circle``
-  ``POV``

You can techncially still use the ``LED*`` versions, but they are
deprecated, so we highly recommend updating to the new names.

Driver names
^^^^^^^^^^^^

Just like the LED handlers, we've dropped ``Driver`` from the names of
most drivers. So, for example,
``bibliopixel.drivers.serial.DriverSerial`` is now simply
``bibliopixel.drivers.serial.Serial``

For the rest of the available drivers, checkout the Wiki
`Drivers <https://github.com/ManiacalLabs/BiblioPixel/wiki/Drivers>`__
page.

SPI Drivers
^^^^^^^^^^^

Speaking of drivers, we have overhauled the SPI (for use on devices like
the Raspberry Pi) in order to consolidate all these similar outputs.
Previously, if you wanted to use, for example, an APA102 LED you would
have to use ``bibliopixel.drivers.APA102.DriverAPA102``, but now all SPI
drivers use the same entry point. Instead you would do the following:

::

    from bibliopixel.drivers.SPI import SPI
    driver = SPI(type='APA102', num=100)

Works with APA102, LPD8806, and WS2801 strips, and and now WS2812 strips
(experimental).

Class and Method Params
^^^^^^^^^^^^^^^^^^^^^^^

Last, please note that some method and class parameters have changed,
mostly from camel case (i.e. ledType) to underscores (i.e. led\_type).
Be sure to check the
`Wiki <https://github.com/ManiacalLabs/BiblioPixel/wiki>`__ for more
details.
