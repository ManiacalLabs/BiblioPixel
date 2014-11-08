from bibliopixel.drivers.visualizer import *
from bibliopixel.led import *
from bibliopixel.animation import *
from matrix_animations import *
from strip_animations import *

driver = DriverVisualizer(width = 96, height = 8, pixelSize = 5)

led = LEDMatrix(driver, rotation = MatrixRotation.ROTATE_0, vert_flip = False)

try:
    scroll = ScrollText(led, "Maniacal Labs Rules!", 32, 0, color = colors.Orange, size = 1)
    bounce = BounceText(led, "Maniacal Labs", 32, 0, color = colors.Orange, size = 1)

    while True:
        led.all_off()
        scroll.run(fps = 20, untilComplete = True, max_cycles = 2)
        led.all_off()
        bounce.run(fps = 20, untilComplete = True, max_cycles = 2)

    print "done!"

except KeyboardInterrupt:
    pass

led.all_off()
led.update()