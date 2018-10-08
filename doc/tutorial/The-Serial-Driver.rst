The Serial Driver
=====================

The Serial Driver handles LEDs that are attached to the computer with the USB
bus, specifically the `AllPixel <https://maniacallabs.com/products/allpixel/>`_ and
`PiPixel <https://www.tindie.com/products/ManiacalLabs/pipixel-raspberry-pi-led-strip-hat/>`_
hardware controllers.

Serial Driver Fields
^^^^^^^^^^^^^^^^^^^^

[TODO-API: embed or point to generated documentation for serial/driver.py]

LEDTYPE
^^^^^^^

The Serial Driver needs to have an LEDTYPE set to identify the LED chipset and
hardware.  This must be one of these values: [TODO-API: point to or embed generated
documentation for ledtype.py]

----

.. code-block:: yaml

   shape: [64, 24]
   animation:
     typename: $bpa.matrix.MathFunc


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/the-serial-driver-footer.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/the-serial-driver-footer.gif
   :alt: Result
   :align: center
