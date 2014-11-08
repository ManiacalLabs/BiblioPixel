from bibliopixel.drivers.network import DriverNetwork
from bibliopixel.led import LEDStrip

#must init with same number of pixels as receiver
driver = DriverNetwork(10, host = "192.168.1.18")
led = LEDStrip(driver)

from bibliopixel.animation import StripChannelTest
anim = StripChannelTest(led)
anim.run()