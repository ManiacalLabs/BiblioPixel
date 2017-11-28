class *bibliopixel.drivers.network.Network*
===========================================

Network allows sending LED data as TCP packets over the network to any
device running a [[NetworkReceiver]] instance or any other receiver that
implements the same `protocol <#protocol>`__. Using this class is
completely abstracted from the actual hardware being controlled, which
is handled instead on the receiving end. It can be used with both
[[Strip]] and [[Matrix]]. Usage is as follows:

.. code:: python

    #receiver.py
    from bibliopixel.drivers.network_receiver import NetworkReceiver
    from bibliopixel.drivers.LPD8806 import *
    from bibliopixel.led import Strip

    #must init with same number of pixels as sender
    driver = LPD8806(100)
    led = Strip(driver)

    receiver = NetworkReceiver(led)
    receiver.start() #returns immediately, must loop or do other work

.. code:: python

    #sender.py
    from bibliopixel.drivers.network import Network
    from bibliopixel.led import Strip

    #must init with same number of pixels as receiver
    driver = Network(100, host = "192.168.1.18")
    led = Strip(driver)

    #run animations here

\_\_init\_\_
^^^^^^^^^^^^

(num = 0, width = 0, height = 0, host = "localhost", port = 3142)

-  **num** - Number of pixels to be controlled.
-  **width** - Width of matrix, optional. Automatically passed to
   [[Matrix]].
-  **height** - Height of matrix, optional. Automatically passed to
   [[Matrix]].
-  **host** - Network name or IP address of the receiver to connect to.
-  **port** - Port number to use. Only need to change if port is already
   in use on the receiving system or if using multiple receivers.

setMasterBrightness
^^^^^^^^^^^^^^^^^^^

(brightness)

-  **brightness** - 8-bit (0-255) brightness value.

When using Nework, calling setMasterBrightness will attempt to pass
along the brightness request to the receiving end and, in turn, along to
the hardware, if supported. If it is supported in the receiving hardware
it will return True, otherwise False.

Protocol
--------

Each packet sent to the network receiver follows the same format:

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
    <td class="header">high byte</td>
    <td class="header">low byte</td>
    <td class="data">n bytes of message data</td>

.. raw:: html

   </tr>

.. raw:: html

   </table>

Command values currently use the following values, as defined in the
CMDTYPE enumeration:

.. code:: python

    class CMDTYPE:
        SETUP_DATA = 1 #reserved for future use
        PIXEL_DATA = 2 #raw pixel data will be sent as [R1,G1,B1,R2,G2,B2,...]
        BRIGHTNESS = 3 #data will be single 0-255 brightness value, length must be 0x00,0x01

After each command is sent, the receiver returns a single byte return
code, as defined by the RETURN\_CODES enumeration:

.. code:: python

    class RETURN_CODES:
        SUCCESS = 255 #All is well
        ERROR = 0 #Generic error
        ERROR_SIZE = 1 #Data receieved does not match given command length
        ERROR_UNSUPPORTED = 2 #Unsupported command
