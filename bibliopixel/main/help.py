PROGRAM = """\

WHAT IS THIS PROGRAM?

This is the frontend to BiblioPixel, the LED control system.

You can use this to run demos or your own projects, to set and get defaults
for projects, or to discover hardware devices attached to your computer.


PROJECTS

BiblioPixel projects are in JSON.  Each project is an object with four named
values called "sections".

  * driver: identifies the hardware driving the LED and its characteristics.
  * layout: represents the geometric layout of the LEDs in one or more drivers.
  * animation: a program that changes the LEDs over time.
  * run: time settings for the animation.

Any of these sections can be omitted, in which case BiblioPixel uses the
default values.

For more information, see
  https://github.com/ManiacalLabs/BiblioPixel/blob/master/README.md

"""
# TODO: finalize URL above.

LOGLEVEL = """\
"""
