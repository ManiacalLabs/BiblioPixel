Projects and settings.
======================

A Project stores all the information about a BiblioPixel project in a
text file in `JSON <http://json.org>`__ format. This is used to create a
library of BiblioPixel projects to access at will.

Example of a project file.
--------------------------

::

    {
        "driver": {
            "typename": "bibliopixel.drivers.SimPixel.DriverSimPixel",
            "num": 12
        },

        "layout": {
            "typename": "bibliopixel.layout.strip.Strip"
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
-------

A project is a JSON object with five named sections.

-  ``driver``: identifies the hardware driving the LED and its
   characteristics.
-  ``layout``: represents the geometric layout of the LEDs in one or
   more drivers.
-  ``animation``: a program that changes the LEDs over time.
-  ``run``: time settings for the animation.
-  ``path``: a list of directories to add to the PYTHONPATH

``driver``, ``layout``, ``animation``, and ``run`` are JSON objects.
``path`` is either a list of strings, or a single string containing a
list of paths separated by colons.

The ``driver``, ``layout`` and ``animation`` sections describe how to
create the BiblioPixel ``Driver``, ``Layout`` or ``Animation`` object
for your project.

Each of these has the special ``typename`` entry: the name of the actual
type of object that's being constructed.

The remaining entries correspond to the arguments to the constructor for
that type.

The ``run`` section's entries are used to call the ``run()`` method on
the ``Animation``.

| The ``path`` section is either a list of directories to be added to
  ``sys.path``, or it's a single string, which is a list of directories
  joined by ``:``.
| These directories are added to ``sys.path`` before your project runs.

So the example above corresponds to the following code:

::

    sys.path.append('/development/BiblioPixelAnimations')
    driver = bibliopixel.drivers.SimPixel.SimPixel(num=12)
    led = bibliopixel.layout.Strip(driver)
    animation = bibliopixel.animation.tests.StripChannelTest(led)
    led.run(max_steps=5)

Projects with multiple drivers.
-------------------------------

An advanced project might need multiple drivers. This is accomplished
with a separate ``drivers`` section, which is just a list of ``driver``
descriptions as described above.

As a convenience, if both the ``driver`` and ``drivers`` sections are
filled in, then the ``driver`` value is used as a set of default values
for each driver in ``drivers``. This avoids duplication in the common
case where there are multiple drivers which only differ a bit.

Examples:

Here's a project which has multiple ``drivers`` and no ``driver``
section:

::

    {
        "drivers": [
            {
                "typename": "serial",
                "width": 32,
                "height": 32,
                "ledtype": "LPD8806",
                "device_id": 10
            },
            {
                "typename": "serial",
                "width": 32,
                "height": 32,
                "ledtype": "LPD8806",
                "device_id": 11
            },
            {
                "typename": "serial",
                "width": 32,
                "height": 32,
                "ledtype": "LPD8806",
                "device_id": 12
            },
        ],

        "layout": "strip",
        "animation": "strip_channel_test"
    }

Here's the same project written using the ``"driver"`` component to
reduce duplication of common entries:

::

    {
        "driver": {
            "typename": "serial",
            "width": 32,
            "height": 32,
            "ledtype": "LPD8806"
        },
        "drivers": [
            {"device_id": 10},
            {"device_id": 11},
            {"device_id": 12}
        ],
        "layout": "strip",
        "animation": "strip_channel_test"
    }
