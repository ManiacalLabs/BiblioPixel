from bibliopixel.drivers.network import Network
from bibliopixel.led import Strip

#must init with same number of pixels as receiver
driver = Network(10, host = "192.168.1.18")
led = Strip(driver)

from bibliopixel.animation import StripChannelTest
anim = StripChannelTest(led)
try:
	anim.run()
except KeyboardInterrupt:
	led.all_off()
	led.update()
