from bibliopixel.drivers.dummy_driver import *
from bibliopixel.drivers.serial_driver import *
w = 26
h = 26
#driver = DriverDummy(w*h, delay=0)
driver = DriverSerial(LEDTYPE.LPD8806, w*h)

from bibliopixel import *
from bibliopixel.animation import *
from matrix_animations import *
import bibliopixel.colors as colors
import bibliopixel.log as log
#log.setLogLevel(log.DEBUG)

class BenchMark(BaseMatrixAnim):
    def __init__(self, led):
        super(BenchMark, self).__init__(led)

    def step(self, amt = 1):
        for y in range(h):
			for x in range(w):
				c = colors.hue2rgb_360(self._step)
				led.set(x, y, c)
				c = led.get(x, y)
				c = colors.hsv2rgb_rainbow((c[2], c[0], c[1]))
				c = colors.hue2rgb_rainbow(c[0])
				c = colors.hue2rgb_spectrum(c[1])
				c = colors.hue2rgb_raw(c[2])
				c = colors.color_scale(c, c[0])
				c = colors.color_scale(c, c[1])
				c = colors.color_scale(c, c[2])
				led.set(x, y, c)

        self._step += 1
        if self._step >= 360:
        	self._step = 0

import time

led = LEDMatrix(driver, width=w, height=h, threadedUpdate=False)
anim = BenchMark(led)

print "Starting non-threaded..."
start = time.time() * 1000.0
anim.run(max_steps=360)
t = (time.time() * 1000.0) - start
print "Time: {:.2f}ms / FPS: {:.2f}".format(t, 360/(t/1000.0))


led = LEDMatrix(driver, width=w, height=h, threadedUpdate=True)
anim = BenchMark(led)

print "Starting threaded..."
start = time.time() * 1000.0
anim.run(max_steps=360)
t = (time.time() * 1000.0) - start
print "Time: {:.2f}ms / FPS: {:.2f}".format(t, 360/(t/1000.0))