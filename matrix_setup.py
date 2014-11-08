#Load driver for your hardware, visualizer just for example
from bibliopixel.drivers.visualizer import DriverVisualizer
driver = DriverVisualizer(width = 10, height = 10, stayTop = True)

#load the LEDMatrix class
from bibliopixel.led import *
#change rotation and vert_flip as needed by your display
led = LEDMatrix(driver, rotation = MatrixRotation.ROTATE_0, vert_flip = False)

#load calibration test animation
from bibliopixel.animation import MatrixCalibrationTest
anim = MatrixCalibrationTest(led)

anim.run()
