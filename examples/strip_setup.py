#Load driver for your hardware, visualizer just for example
from bibliopixel.drivers.visualizer import DriverVisualizer
driver = DriverVisualizer(num = 10)

#load the LEDStrip class
from bibliopixel.led import *
led = LEDStrip(driver)

#load channel test animation
from bibliopixel.animation import StripChannelTest
anim = StripChannelTest(led)

try:
	anim.run()
except KeyboardInterrupt:
	led.all_off()
	led.update()

