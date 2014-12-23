#Load driver for your hardware, visualizer just for example

import bibliopixel.log as log
log.setLogLevel(log.DEBUG)

# from bibliopixel.drivers.visualizer import DriverVisualizer
# #driver = DriverVisualizer(width = 10, height = 10, stayTop = True)
# driver1 = DriverVisualizer(width=16, height=16, port=1611, stayTop=True)
# driver2 = DriverVisualizer(width=16, height=16, port=1612, stayTop=True)
# driver3 = DriverVisualizer(width=32, height=16, port=1613, stayTop=True)
# #driver4 = DriverVisualizer(width=12, height=12, port=1614)

from bibliopixel.drivers.serial_driver import *
driver1 = DriverSerial(LEDTYPE.LPD8806, 24*24, deviceID = 2, SPISpeed = 2)
driver2 = DriverSerial(LEDTYPE.LPD8806, 24*24, deviceID = 12, SPISpeed = 2)

#load the LEDMatrix class
from bibliopixel.led import *
#change rotation and vert_flip as needed by your display
build = MultiMapBuilder()
build.addRow(mapGen(24,24))
build.addRow(mapGen(24,24))#, mapGen(12,12))
led = LEDMatrix(driver = [driver1,driver2], width = 24, height = 48, coordMap=build.map, threadedUpdate = False)

try:
	#load calibration test animation
	# from bibliopixel.animation import MatrixCalibrationTest
	# anim = MatrixCalibrationTest(led)

	from matrix_animations import *
	# anim = ScrollText(led, "Maniacal Labs", xPos=20, yPos=1, color=colors.Orange, bgcolor=colors.Off, size=2)
	# anim.run(amt=1, fps=15)

	anim = Bloom(led, dir=True)
	anim.run(amt=6, fps=30)

	# from bibliopixel.image import *
	# anim = ImageAnim(led, "C:/SVN/BiblioPixelExamples/anims/YoshiRotating.gif", offset=(0, 0), bgcolor=colors.Off, brightness=255)
	# anim.run()
except KeyboardInterrupt:
	led.all_off()
	led.update()

