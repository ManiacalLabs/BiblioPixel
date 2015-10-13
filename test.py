from bibliopixel.drivers.visualizer import DriverVisualizer
from bibliopixel import LEDStrip, LEDMatrix
import bibliopixel.colors as colors
import time

driver = DriverVisualizer(num=60, width=0, height=0, pixelSize=15, port=1618, stayTop=False)
led = LEDStrip(driver, threadedUpdate=False, masterBrightness=255, pixelWidth=6)

col = [colors.Red, colors.Orange, colors.Yellow, colors.Green, colors.Blue, colors.Purple]

pixel = 0
for c in col:
    led.set(pixel, c)
    pixel += 1
#print len(led.buffer)
led.update()
