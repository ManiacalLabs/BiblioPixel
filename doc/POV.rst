class *bibliopixel.POV*
=======================

POV provides methods to control persistence of vision (POV) displays,
which are built from a single, in motion, strip. It inherits from
[[Matrix]] and provides a logical matrix on which to write pixel data,
but then displays that data one vertical column at a time onto the
strip. So the display should be built from a strip that contains a
number of pixels equal to the vertical height of the desired matrix,
while the width is arbitrary and dependent on time and speed. For a
great example of a POV display and the usage of this class, check out
the `POVStick
project <http://maniacallabs.com/2014/11/19/weekend-project-povstick/>`__.
POV actually lives at bibliopixel.led.POV but can be accessed at
bibiliopixel.POV for convenience.

\_\_init\_\_
^^^^^^^^^^^^

(driver, povHeight, width, rotation = Rotation.ROTATE\_0, vert\_flip =
False, masterBrightness=255)

-  **driver** - A driver class or list of driver classes that inherit
   from bibliopixel.drivers.[[DriverBase]]. See the [[Drivers]] page for
   more info.
-  **povHeight** - height (y-axis) of the POV display. In this case,
   this must be the actual pixel count of the attached LED strip.
-  **width** - logical width (x-axis) of the matrix. Because the display
   is actually 1 dimensional, this width only exists in memory and can
   be however wide the desired width of the virtual display is.
-  **rotation** - Amount to rotate matrix coordinate map by in order for
   coordinate (0,0) to be the Top-Left corner of the display. See
   [[Matrix Orientation\|Display-Setup#matrix-orientation]] for more
   details.
-  **vert\_flip** - True to flip the matrix coordinate map on the
   y-axis. See [[Matrix Orientation\|Display-Setup#matrix-orientation]]
   for more details.
-  **brightness** - Default master brightness value, 0-255

All drawing methods from [[Matrix]] are available for use with POV. It
does however, overwrite the normal update method. Currently none of the
animation classes properly handle POV because there is no way to set how
long each frame displays for. Because of this, they will simply display
each vertical column as fast as possible. [[BasePOVAnim]] will likely be
created in the near future to fix this. For now, the best way to use POV
is to load or generate a single image and then call the update method
directly, like this:

.. code:: python

    from bibliopixel.led import *
    import bibliopixel.image as img
    from bibliopixel.drivers.serial_driver import *
    import bibliopixel.gamma as gamma

    i = img.Image.open("povimage.png")

    img_width = i.size[0]
    totalFrameTime = img_width * col_time

    print "Image Display Time: {0:.1f}s".format(totalFrameTime/1000.0)

    driver = Serial(LEDTYPE.LPD8806, num = 96)

    #automatically configure matrix width to image width.
    #change povHeight to match your setup
    led = POV(driver, povHeight = 96, width = img_width, rotation=MatrixRotation.ROTATE_0, vert_flip=True)
    led.setMasterBrightness(bright)

    img.showImage(led, imageObj = i, bgcolor=bgcolor)

    try:
        while True:
            led.update(frameTime=totalFrameTime)
    except KeyboardInterrupt:
        led.all_off()
        led.update()

update
^^^^^^

(frameTime = None):

-  **frameTime** - The total time (in milliseconds) over which to
   display the current frame. This time will be divided by the width and
   each vertical column will be shown for that amount of time. This is
   great for dialing in the display time with the speed at which the
   LEDs are moving to generate the desired image size. Also, when taking
   a long exposure to capture the POV image, the exposure time should be
   set to some amount of time *greater* than frameTime.

Properties
~~~~~~~~~~

--------------

All properties from [[Matrix]] are available for use with POV:
