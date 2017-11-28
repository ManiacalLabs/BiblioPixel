Drivers are what make BiblioPixel so flexible. All the work of
generating pixel data can be completely abstracted away from the
hardware while the drivers handle actually doing something with that
data, no matter what that may be.

Currently, the included drivers are:

-  
-  
-  
-  
-  
-  
-  [[Serial]]: For interfacing with serial controllers, like the
   `AllPixel <http://maniacallabs.com/AllPixel>`__.
-  
-  
-  

These are all very useful, but what makes the driver system even more
useful is the ability to write your own. This is made easy by the
[[DriverBase]] base-class, for example:

.. code:: python

    from bibliopixel.drivers.driver_base import *

    class DriverTest(DriverBase):
        def __init__(self, num, gamma = None):
            super(DriverTest, self).__init__(num, gamma)
            #do any other initialization here

        #Push new data
        def update(self, data):
        #handle channel order and gamma correction
            self._fixData(data)
            #output to hardware/UI/etc.
            print(data)

The above is all that is needed for a working driver, aside from the
actual implementation of interfacing with your hardware, UI, etc. For
more complicated setups, see [[DriverBase]] for available properties and
methods that can be overridden.

[[DriverSPIBase]] is also provided for creating drivers using direct SPI
port access on devices like the Raspberry Pi and Beagle Bone Black. For
example, the WS2801 driver:

.. code:: python

    from bibliopixel.drivers.spi_driver_base import *

    class WS2801(DriverSPIBase):
        def __init__(self, num, c_order = ChannelOrder.RGB, use_py_spi = True, dev="/dev/spidev0.0", SPISpeed = 1, gamma = None):
            if SPISpeed > 1 or SPISpeed <= 0:
                raise ValueError("WS2801 requires an SPI speed no greater than 1MHz or SPI speed was set <= 0")
            super(WS2801, self).__init__(num, c_order = c_order, use_py_spi = use_py_spi, dev = dev, SPISpeed = SPISpeed, gamma)

The WS2801 chipset has a very simple protocol so no changes to the
update() method are needed. All the hard work of SPI setup and
communication is handled by [[DriverSPIBase]]. If a more complicated
data format is needed, modify the data buffer in \_\_init\_\_() or
override update() and modify [[self.\_buf\|DriverBase#\_buf]] before
calling [[self.\_sendData()\|driverspibase#\_senddata]], which is
normally called automatically in the default update() implementation.
