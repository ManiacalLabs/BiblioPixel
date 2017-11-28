Most situations call for more than one animation and the ability to
control what order the animations run in, for how long, how fast, etc.
While you can certainly just add one animation after another in your
code, sometimes it's better to have a single point of control. This is
where [[AnimationQueue\|Animations#class-animationqueue]] comes in.
Below is a basic example of controlling three animations in a queue:

.. code:: python

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

`Download Example <examples/AnimationQueue.py>`__

Queued animations can either be given an explicit framerate or use a
global framerate set on the queue by leaving the fps parameter as None.
When the AnimationQueue is run, it will loop unless untilComplete is set
to True. If it is stopped and restarted later, it will always start at
the beginning of the queue, not where it left off.
