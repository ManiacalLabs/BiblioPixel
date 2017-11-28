#import base classes and driver
from bibliopixel import *
from bibliopixel.drivers.visualizer import Visualizer

#import AnimationQueue
from bibliopixel.animation import AnimationQueue

#import animations
from BiblioPixelAnimations.matrix.bloom import Bloom
from BiblioPixelAnimations.matrix.GameOfLife import GameOfLife
from BiblioPixelAnimations.matrix.pinwheel import Pinwheel

#load driver and controller and animation queue
driver = Visualizer(width=10, height=10, stayTop=True)
led = Matrix(driver)
anim = AnimationQueue(led)

#Load animations into Queue
bloom = Bloom(led)
#run at 15fps, for 10 seconds
anim.addAnim(bloom, amt=6, fps=15, max_steps=150)

gol = GameOfLife(led)
#run at queue default framerate, until simulation completes twice
anim.addAnim(gol, fps=None, untilComplete=True, max_cycles=2)

pin = Pinwheel(led)
#run at queue default framerate for 300 steps
anim.addAnim(pin, amt=4, fps=None, max_steps=300)

#run animations at default 30fps
anim.run(fps=30)
