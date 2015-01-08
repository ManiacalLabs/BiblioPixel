#Load driver for your hardware, visualizer just for example
#from bibliopixel.drivers.visualizer import DriverVisualizer
#driver = DriverVisualizer(num = 10)


    # GENERIC = 0 #Use if the serial device only supports one chipset
    # LPD8806 = 1
    # WS2801  = 2
    # #These are all the same
    # WS2811 = 3
    # WS2812 = 3
    # WS2812B = 3
    # NEOPIXEL = 3
    # APA104 = 3
    # #400khz variant of above
    # WS2811_400 = 4

    # TM1809 = 5
    # TM1804 = 5
    # TM1803 = 6
    # UCS1903 = 7
    # SM16716 = 8
    # APA102 = 9
    # LPD1886 = 10 
    # P9813 = 11 
from bibliopixel.drivers.serial_driver import *
driver = DriverSerial(LEDTYPE.APA102, 700)

#load the LEDStrip class
from bibliopixel.led import *
led = LEDStrip(driver, threadedUpdate=True)
led.setMasterBrightness(64)
import bibliopixel.log as log
log.setLogLevel(log.DEBUG)

#load channel test animation
from bibliopixel.animation import StripChannelTest
#anim = StripChannelTest(led)

from strip_animations import *
anim = RainbowCycle(led)

anim.run()

