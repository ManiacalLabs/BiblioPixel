#!/usr/bin/env python3

# This must be run separately from the command line like this:
#
#   $ scripts/release_test/tests/classic.py

import bibliopixel
from bibliopixel.drivers.simpixel import SimPixel

bibliopixel.log.setLogLevel(bibliopixel.log.DEBUG)

# set number of pixels & LED type here
driver = SimPixel(num=32)

# load the LEDStrip class
from bibliopixel.layout import Strip
led = Strip(driver)

# load channel test animation
from bibliopixel.animation import StripChannelTest
anim = StripChannelTest(led)

try:
    # run the animation
    anim.run()

except KeyboardInterrupt:
    # Ctrl+C will exit the animation and turn the LEDs offs
    led.all_off()
    led.update()
