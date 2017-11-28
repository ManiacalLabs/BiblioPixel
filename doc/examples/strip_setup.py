#Load driver for your hardware, visualizer just for example
from bibliopixel.drivers.visualizer import Visualizer
driver = Visualizer(num = 10)

#load the Strip class
from bibliopixel.led import *
led = Strip(driver)

#load channel test animation
from bibliopixel.animation import StripChannelTest
anim = StripChannelTest(led)

try:
	anim.run()
except KeyboardInterrupt:
	led.all_off()
	led.update()
