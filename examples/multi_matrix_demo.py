#Load driver for your hardware, visualizer just for example
import time
import bibliopixel.log as log
log.setLogLevel(log.DEBUG)

from bibliopixel.drivers.serial_driver import *
from bibliopixel.drivers.visualizer import *

#global vars
ledtype = LEDTYPE.NEOPIXEL
w = 24
h = 24
driverCount = 2
numFrames = 100

#Use DeviceIDManager.py to set or view your device IDs

drivers = []
for i in range(1, driverCount+1):
	#drivers.append(DriverVisualizer(width=w, height=h, port=1610+i, pixelSize = 8, stayTop=True))
	drivers.append(DriverSerial(ledtype, w*h, deviceID = i, SPISpeed = 2))

#load the LEDMatrix class
from bibliopixel.led import *
import bibliopixel.colors as colors
#change rotation and vert_flip as needed by your display
build = MultiMapBuilder()
for d in drivers:
	build.addRow(mapGen(w,h,rotation=MatrixRotation.ROTATE_0))

led = LEDMatrix(driver = drivers, threadedUpdate = True, width = w, height = h*len(drivers), coordMap=build.map)

try:
	from matrix_animations import *

	led.setMasterBrightness(255)

	anim = Bloom(led, dir=True)
	start = time.time() * 1000.0
	anim.run(amt=6, max_steps = numFrames)
	t = (time.time() * 1000.0) - start
	print "Time: {:.2f}ms / FPS: {:.2f}".format(t, numFrames/(t/1000.0))
	led.all_off()
	led.update()

except KeyboardInterrupt:
	pass

led.all_off()
led.update()
time.sleep(1)

