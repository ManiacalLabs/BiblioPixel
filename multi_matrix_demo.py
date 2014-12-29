#Load driver for your hardware, visualizer just for example
import time
import bibliopixel.log as log
log.setLogLevel(log.DEBUG)

from bibliopixel.drivers.serial_driver import *

ledtype = LEDTYPE.NEOPIXEL
w = 25
h = 25
driverCount = 4
numFrames = 1000

# from bibliopixel.drivers.visualizer import DriverVisualizer
# drivers = [
# 	DriverVisualizer(width=24, height=24, port=1611, pixelSize = 5, stayTop=True),
# 	DriverVisualizer(width=24, height=24, port=1612, pixelSize = 5,  stayTop=True),
# 	DriverVisualizer(width=24, height=24, port=1613, pixelSize = 5,  stayTop=True),
# 	DriverVisualizer(width=24, height=24, port=1614, pixelSize = 5,  stayTop=True),
# ]

#Use DeviceIDManager.py to set or view your device IDs

drivers = []
for i in range(1, driverCount+1):
	drivers.append(DriverSerial(ledtype, w*h, deviceID = i, SPISpeed = 2))

#load the LEDMatrix class
from bibliopixel.led import *
import bibliopixel.colors as colors
#change rotation and vert_flip as needed by your display
build = MultiMapBuilder()
for d in drivers:
	build.addRow(mapGen(w,h,rotation=MatrixRotation.ROTATE_270))

led = LEDMatrix(driver = drivers, threadedUpdate = True, width = w, height = h*len(drivers), coordMap=build.map)

try:
	#load calibration test animation
	# from bibliopixel.animation import MatrixCalibrationTest
	# anim = MatrixCalibrationTest(led)

	from matrix_animations import *

	led.setMasterBrightness(32)


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

