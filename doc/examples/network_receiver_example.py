from bibliopixel.drivers.network_receiver import NetworkReceiver
from bibliopixel.drivers.visualizer import *
from bibliopixel.led import Strip

#must init with same number of pixels as sender
driver = Visualizer(10)
led = Strip(driver)

receiver = NetworkReceiver(led)

try:
    receiver.start(join = True) #join = True causes it to not return immediately
except KeyboardInterrupt:
    receiver.stop()
    pass
