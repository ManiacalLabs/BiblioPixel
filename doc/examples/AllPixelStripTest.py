#Load driver for your hardware, visualizer just for example
from bibliopixel.drivers.serial_driver import *
#set your LED type here
driver = Serial(num = 10, type = LEDTYPE.LPD8806)

#load the LEDStrip class
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
