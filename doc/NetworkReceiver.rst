class *bibliopixel.drivers.network\_receiver.NetworkReceiver*
=============================================================

NetworkReceiver allows receiving LED data as TCP packets over the
network from [[Network]] or any other sender that implements the same
[[protocol\|Network#protocol]]. Usage is as follows:

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

\_\_init\_\_(led, port = 3142, interface = '0.0.0.0')
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  **led** - Instance of [[Strip]] or [[Matrix]] to send the received
   LED data to.
-  **port** - Port number to use. Only need to change if port is already
   in use or if using multiple receivers.
-  **interface** - Network interface for the receiver to listen on. By
   default all available interfaces are used. Set this to 'localhost' to
   only accept connections from the current system.

start(join = False)
^^^^^^^^^^^^^^^^^^^

-  **join** - True causes this method to block until the receiver thread
   ends.

Starts the receiver thread and returns unless join == True.

stop()
^^^^^^

Stops the receiver thread and closes all connections.
