from bibliopixel.drivers.visualizer import DriverVisualizer
from bibliopixel import LEDStrip, LEDMatrix
import bibliopixel.colors as colors
import time

driver = DriverVisualizer(width=12, height=12, pixelSize=15, port=1618, stayTop=False)
led = LEDStrip(driver, threadedUpdate=False, masterBrightness=255, pixelWidth=6)
led = LEDMatrix(driver, pixelSize=(3,4))

col = [colors.Red, colors.Orange, colors.Yellow, colors.Green, colors.Blue, colors.Purple]

#pixel = 0
# for c in col:
#     led.set(pixel, c)
#     pixel += 1
# #print len(led.buffer)
cols = [colors.Red, colors.Green]
for x in range(4):
    for y in range(4):
        c = cols[(x+y)%2]

        led.setRGB(x,y,c[0], c[1], c[2])

print (led.width, led.height, led.numLEDs)
led.update()
