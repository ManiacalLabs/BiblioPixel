Projects and settings.
====

A Project stores all the information about a BiblioPixel project in a
text file in [JSON](http://json.org) format. This is used to create a
library of BiblioPixel projects to access at will.

Example of a project file.
----

    {
        "driver": {
            "typename": "bibliopixel.drivers.SimPixel.DriverSimPixel",
            "num": 12
        },

        "led": {
            "typename": "bibliopixel.led.strip.LEDStrip"
        },

        "animation": {
            "typename": "bibliopixel.animation.tests.StripChannelTest"
        },

        "run": {
            "max_steps": 5
        },

        "path": "/development/BiblioPixelAnimations"
    }

Details
----

A project is a JSON object with five named sections.

  * driver: identifies the hardware driving the LED and its characteristics.
  * led: represents the geometric layout of the LEDs in one or more drivers.
  * animation: a program that changes the LEDs over time.
  * run: time settings for the animation.
  * path: a list of directories to add to the PYTHONPATH

The first four sections are JSON objects.

The `driver`, `led` and `animation` sections describe how to create the
BiblioPixel `Driver`, `LED` or `Animation` object for your project.

Each of these has the special `typename` entry: the name of the actual type
of object that's being constructed.

The remaining entries correspond to the arguments to the constructor for that
type.

The `run` section's entries are used to call the `run()` method on the
`Animation`.

The `path` section is either a list of directories to be added to `sys.path`,
or it's a single string, which is a list of directories joined by `:` which are
to be added to `sys.path`.


So the example above corresponds to the following code:

    sys.path.append('/development/BiblioPixelAnimations')
    driver = bibliopixel.drivers.SimPixel.DriverSimPixel(num=12)
    led = bibliopixel.led.strip.LEDStrip(driver)
    animation = bibliopixel.animation.tests.StripChannelTest(led)
    led.run(max_steps=5)
