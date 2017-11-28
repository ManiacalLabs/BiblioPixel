class *bibliopixel.drivers.serial.Serial*
=========================================

Serial allows for the control of the
`AllPixel <http://maniacallabs.com/AllPixel>`__ or any other serial
device that implements the same `protocol <#protocol>`__.

``pyserial`` is required. Install with
``pip install pyserial --upgrade``. If you are running on a Raspberry
Pi, pyserial is already installed but it's too old and owned by the OS.
To upgrade, use
``sudo pip install pyserial --upgrade --ignore-installed``

\_\_init\_\_
^^^^^^^^^^^^

(ledtype, num, dev="", c\_order = ChannelOrder.RGB, SPISpeed = 16, gamma
= None, restart\_timeout = 3, device\_id = None, hardwareID =
"1D50:60AB", baudrate=921600)

-  **ledtype** - Type of LEDs being controlled by the serial hardware.
   See `LED Types <#led-types>`__ for more info.
-  **num** - Number of pixels to be controlled.
-  **dev** - The name of the COM port to be used. If using the
   `AllPixel <http://maniacallabs.com/AllPixel>`__ this can be left
   blank and the port name will be automatically detected.
-  **c\_order** - Optional: Channel order used by the attached display.
   Can be any of the six options in the ChannelOrder class. See
   [[Channel Order\|Display-Setup#channel-order]] for more details.
-  **spi\_speed** - Optional. The SPI speed, in MHz, to use when
   communicating with SPI-based strips. Valid range; 1-24.
-  **gamma** - 256 value gamma correction list. The list *MUST* contain
   256 8-bit integer values. Predefined corrections lists can be found
   in [[bibliopixel.gamma\|Gamma-Correction]]
-  **restart\_timeout** - Number of seconds to wait after
   reconfiguration and restarting the device before trying to reconnect.
   Some systems take longer to re-enumerate the device and, if so,
   increase this value. However, if a reconfigure is needed and
   reconnect fails it does not mean the reconfigure failed. Increasing
   this value is not necessarily needed, but just restarting the script
   instead.
-  **device\_id** - User-set unique ID of the device to connect to. See
   [[Device ID]] for more details.
-  **hardwareID** - USB Vendor ID and Product ID of the device, in
   "VID:PID" form. This is used to auto-detect a connected device based
   on it's Vendor and Product information. This defaults to the VID/PID
   pair of the `AllPixel <http://maniacallabs.com/AllPixel>`__ but this
   parameter is provided to override the value if using another device.
-  **baudrate** - Serial speed to connect to the device at. Not required
   for the AllPixel.

set\_brightness
^^^^^^^^^^^^^^^

(brightness)

-  **brightness** - 8-bit (0-255) brightness value.

When using Serial, calling set\_brightness will attempt to pass along
the brightness request to the hardware, if supported. If it is supported
in the receiving hardware it will return True, otherwise False.

LED Types
---------

The "type" parameter of the
`init <#__init__type-num-dev-c_order--channelorderrgb-spispeed--16-gamma--none>`__
method from above should be an integer value, representing chipsets
supported by the serial hardware. The list below is specifically for the
`AllPixel <http://maniacallabs.com/AllPixel>`__ but if other chipsets
values are needed, any integer value can be passed instead of using the
LEDTYPE enumeration. The intent is that the serial device may support
multiple chipsets and this value allows configuring which chipset is
used at run-time. A type value of 0 can be used if the device only
supports one chipset.

.. code:: python

    class LEDTYPE:
        GENERIC = 0 #Use if the serial device only supports one chipset
        LPD8806 = 1
        WS2801  = 2
        #These are all the same
        WS2811 = 3
        WS2812 = 3
        WS2812B = 3
        NEOPIXEL = 3
        #400khz variant of above
        WS2811_400 = 4

        TM1809 = 5
        TM1804 = 5
        TM1803 = 6
        UCS1903 = 7
        SM16716 = 8

Protocol
--------

Each packet sent to the serial device follows the same format:

.. raw:: html

   <table>

.. raw:: html

   <tr>

::

    <td class="header">command</td>
    <td class="header" colspan=2>length (n)</td>
    <td class="data">data</td>

.. raw:: html

   </tr>

.. raw:: html

   <tr>

::

    <td class="header">0 to 255</td>
    <td class="header">low byte</td>
    <td class="header">high byte</td>
    <td class="data">n bytes of message data</td>

.. raw:: html

   </tr>

.. raw:: html

   </table>

Command values currently use the following values, as defined in the
CMDTYPE enumeration:

.. code:: python

    class CMDTYPE:
        SETUP_DATA = 1 #config data (LED type, SPI speed, num LEDs)
        PIXEL_DATA = 2 #raw pixel data will be sent as [R1,G1,B1,R2,G2,B2,...]
        BRIGHTNESS = 3 #data will be single 0-255 brightness value, length must be 0x00,0x01

After each command is sent, the receiver returns a single byte return
code, as defined by the RETURN\_CODES enumeration:

.. code:: python

    class RETURN_CODES:
        SUCCESS = 255 #All is well
        REBOOT = 42 #Device reboot needed after configuration
        ERROR = 0 #Generic error
        ERROR_SIZE = 1 #Data receieved does not match given command length
        ERROR_UNSUPPORTED = 2 #Unsupported command
        ERROR_PIXEL_COUNT = 3 #Too many pixels for device

**Note:** ERROR\_PIXEL\_COUNT is returned after connecting and
configuring a device, waiting for the reboot, and connecting again. The
pixel memory allocation is dynamic and happens at reboot. In order to
not require a hard coded pixel limit (a value which can change with
custom versions of the firmware) the limit is detected on boot. If the
requested count is beyond the limit, ERROR\_PIXEL\_COUNT will be
returned upon connect and the device will revert to the default
configuration.
