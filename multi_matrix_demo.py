#Load driver for your hardware, visualizer just for example
import time
import bibliopixel.log as log
log.setLogLevel(log.DEBUG)

from bibliopixel.drivers.serial_driver import *

ledtype = LEDTYPE.NEOPIXEL
w = 16
h = 16
# from bibliopixel.drivers.visualizer import DriverVisualizer
# drivers = [
# 	DriverVisualizer(width=24, height=24, port=1611, pixelSize = 5, stayTop=True),
# 	DriverVisualizer(width=24, height=24, port=1612, pixelSize = 5,  stayTop=True),
# 	DriverVisualizer(width=24, height=24, port=1613, pixelSize = 5,  stayTop=True),
# 	DriverVisualizer(width=24, height=24, port=1614, pixelSize = 5,  stayTop=True),
# ]

#Use DeviceIDManager.py to set or view your device IDs

drivers = [
	#DriverSerial(ledtype, w*h, deviceID = 1, SPISpeed = 2),
	# DriverSerial(ledtype, w*h, deviceID = 2, SPISpeed = 2),
	DriverSerial(ledtype, w*h, deviceID = 3, SPISpeed = 2),
	# DriverSerial(ledtype, w*h, deviceID = 4, SPISpeed = 2),
]

#load the LEDMatrix class
from bibliopixel.led import *
#change rotation and vert_flip as needed by your display
build = MultiMapBuilder()
for d in drivers:
	build.addRow(mapGen(w,h))

led = LEDMatrix(driver = drivers, width = w, height = h*len(drivers), coordMap=build.map, threadedUpdate = True)

try:
	#load calibration test animation
	# from bibliopixel.animation import MatrixCalibrationTest
	# anim = MatrixCalibrationTest(led)

	from matrix_animations import *
	# anim = ScrollText(led, "Maniacal Labs", xPos=20, yPos=1, color=colors.Orange, bgcolor=colors.Off, size=2)
	# anim.run(amt=1, fps=15)

	led.setMasterBrightness(64)

	anim = Bloom(led, dir=True)
	start = time.time() * 1000.0
	anim.run(amt=6, max_steps = 100)
	print (time.time() * 1000.0) - start
	#led.all_off()
	#led.update()

	# from bibliopixel.image import *
	# anim = ImageAnim(led, "C:/SVN/BiblioPixelExamples/anims/YoshiRotating.gif", offset=(0, 0), bgcolor=colors.Off, brightness=255)
	# anim.run()
except KeyboardInterrupt:
	pass

led.all_off()
led.update()
time.sleep(1)

