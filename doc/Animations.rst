Module *animation*
==================

The animation module provides base classes upon which to build custom
animation routines. Animations built from these classes can be run with
only two lines of code and continue running based on a wide array of
options. For example:

.. code:: python

    anim = StripChannelTest(led)
    anim.run()

This will run StripChannelTest continuously and as fast as possible.

For more information on using the animation classes, see [[Writing an
Animation]].

Class *BaseAnimation*
---------------------

BaseAnimation serves as the basis for
`BaseStripAnim <#class-basestripanim>`__ and
`BaseMatrixAnim <#class-basematrixanim>`__ and should not be inherited
from directly. It simply provides any code that is shared between
`BaseStripAnim <#class-basestripanim>`__ and
`BaseMatrixAnim <#class-basematrixanim>`__.

\_\_init\_\_
^^^^^^^^^^^^

(led)

-  **led** - An instance of [[Matrix]] or [[Strip]]

preRun
^^^^^^

By default, preRun does nothing but can be overridden by any class that
inherits from `BaseStripAnim <#class-basestripanim>`__ and
`BaseMatrixAnim <#class-basematrixanim>`__. If overridden, if will
always be called at the beginning of each call to `run() <#run>`__. This
is mainly provided as a way to always initialize to a proper state
without the user of your animation class having to call anything except
`run() <#run>`__.

preStep
^^^^^^^

By default, preStep does nothing but can be overridden by any class that
inherits from `BaseStripAnim <#class-basestripanim>`__ and
`BaseMatrixAnim <#class-basematrixanim>`__. If overridden, if will
always be called at the beginning of each call to `step() <#step>`__.
This is mainly provided as a way to always initialize to a proper state
without the user of your animation class having to call anything except
`step() <#step>`__.

step
^^^^

(amt = 1)

-  **amt** - Amount to increment `\_step <#_step>`__ by after each call
   to step(). Increments by 1 by default. As step() is generally called
   by `run() <#run>`__, this value will be set to whatever is passed
   into `run() <#run>`__. This parameter is required by can be ignored
   by your step() implementation. Actually incrementing
   `\_step <#_step>`__ is the responsibility of the animation author.

step() *MUST* be overridden for an animation class otherwise it will
throw an exception. This is where all of the work is actually done to
generate the animation frame. The frame should only be generated here.
Updating of the display will occur in `run() <#run>`__.

.. code:: python

    def step(self, amt = 1):
        self.layout.fill((self._step, 0, 0))
        self._step += amt
        if self._step > 255:
            self._step = 0

The above step() implementation will fill the entire display with
increasing brightness values of red, wrapping around to 0% once it
reaches maximum brightness.

run
^^^

(amt = 1, fps=None, sleep=None, max\_steps = 0, untilComplete = False,
max\_cycles = 0, threaded = False, joinThread = False)

-  **amt** - Amount to increment `\_step <#_step>`__ after each frame is
   generated. Can be used to run the animation faster without changing
   the framerate by skipping frames.
-  **fps** - Target frames per second to run the animation at.
   Guaranteed to not run faster but may not run as fast as set if the
   frame generation and display update takes too long. Ignored if sleep
   is set.
-  **sleep** - Amount of time, in milliseconds, between each frame,
   including the time it takes to generate the frame and update the
   display. fps is ignored if sleep is set.
-  **max\_steps** - How many total steps to run the animation for before
   automatically quitting. This is incremented on its own and is not
   effected by amt.
-  **untilComplete** - True/False: Run the animation until
   `animComplete <#animcomplete>`__ flag is set by the animation itself.
-  **max\_cycles** - Only used with untilComplete. If set above 0, the
   animation will run until `animComplete <#animcomplete>`__ flag has
   been set that many times.
-  **threaded** - Setting to True will run the animation on a separate
   thread and return immediately, unless joinThread is set. The script
   or application must not close while the animation is threaded.
   **NOTE:** You *cannot* run multiple animations at the same time! They
   *will not* superimpose on themselves. Instead it will cause a failure
   when trying to update the display. This is intended for doing other,
   *non-animation* things while the animation is running.
-  **joinThread** - If *threaded* is True, setting this to True will run
   the animation on another thread but run() will *not* return until the
   animation has completed or is stopped.

Properties
~~~~~~~~~~

--------------

:raw-latex:`\layout`
^^^^^^^^^^^^^^^^^^^^

Instance of [[Layout]] that was passed into the animation.

\_step
^^^^^^

The current frame step which can be used for keeping track of the
animation state and is incremented in `step() <#step>`__

internal\_delay
^^^^^^^^^^^^^^^

This can be set to a number of milliseconds by the animation itself to
override any fps or sleep settings. Mainly it is to be used for
animations that require variable timing between each frame.

completed
^^^^^^^^^

Set to True to flag the animation sequence as complete and use with the
``completed`` option when running the animation.

Class *BaseStripAnim*
---------------------

BaseStripAnim is the basis for any animation that runs with an instance
of [[Strip]] and provides all the same methods and properties as
`BaseAnimation <#class-baseanimation>`__ plus those below.

\_\_init\_\_
^^^^^^^^^^^^

(layout, start=0, end=-1)

-  **layout** - An instance of [[Strip]]
-  **start** - Pixel index to start the animation at, defaults to 0
-  **end** - Pixel index to end the animation at. It left at -1, it will
   default to the last pixel on the strip.

Note: The start and end parameters must be respected by the inheriting
animation for them to do anything.

Properties
~~~~~~~~~~

--------------

In addition to the properties provided by
`BaseAnimation <#class-baseanimation>`__, the following properties are
available to classes that inherit from
`BaseStripAnim <#class-basestripanim>`__.

\_start
^^^^^^^

Index of the first pixel to start the animation at. This does not have
to be used by an animation class but it is recommended that it be
respected.

\_end
^^^^^

Index of the last pixel to end the animation at. This does not have to
be used by an animation class but it is recommended that it be
respected.

\_size
^^^^^^

The calculated size of the total animation space, (\_end - \_start)

Class *BaseMatrixAnim*
----------------------

BaseStripAnimation is the basis for any animation that runs with an
instance of [[Strip]] and provides all the same methods and properties
as `BaseAnimation <#class-baseanimation>`__ plus those below.

\_\_init\_\_
^^^^^^^^^^^^

(layout, width=0, height=0, startX=0, startY=0)

-  **layout** - An instance of [[Matrix]]
-  **width** - Width of the pixel matrix. If 0, width will be retrieved
   from the led instance.
-  **height** - Height of the pixel matrix. If 0, height will be
   retrieved from the led instance.
-  **startX** - X coordinate to start the animation at.
-  **startY** - Y coordinate to start the animation at.

Note: The startX and startY parameters must be respected by the
inheriting animation for them to do anything.

Properties
~~~~~~~~~~

--------------

In addition to the properties provided by
`BaseAnimation <#class-baseanimation>`__, the following properties are
available from `BaseMatrixAnim <#class-basematrixanim>`__.

width
^^^^^

Width of the pixel matrix to use with the animation.

height
^^^^^^

Height of the pixel matrix to use with the animation.

startX
^^^^^^

X coordinate to start the animation at. This does not have to be used by
an animation class but it is recommended that it be respected.

startY
^^^^^^

Y coordinate to start the animation at. This does not have to be used by
an animation class but it is recommended that it be respected.

Class *BaseGameAnim*
--------------------

BaseGameAnim is the basis for interactive animations and inherits from
`BaseMatrixAnim <#class-basematrixanim>`__, providing all the same
methods and properties. However, it also provides automatic handling for
inputs and speed timing. It is highly recommended that game animations
be designed to run at a specific frame-rate as the timing is based off
of frames, not actual clock time. Max speed will depending on the
performance of your display but 30fps has been found to work well in
most cases.

\_\_init\_\_
^^^^^^^^^^^^

(layout, inputDev)

-  **layout** - An instance of [[Matrix]]
-  **inputDev** - An input device class object that inherits from
   [[BaseGamePad\|GamePad#class-basegamepad]]. This is required to get
   control input for the animation.

checkSpeed
^^^^^^^^^^

(name)

-  **name** - Name of the timing object to check as setup by
   `setSpeed <#setspeed>`__

checkSpeed can be used in your animation inside of the
`step() <#step>`__ method to determine if something should change on
that frame, such as moving a sprite.

setSpeed
^^^^^^^^

(name, speed)

-  **name** - Name for this timing object. Used to check via
   `checkSpeed <#checkspeed>`__.
-  **speed** - Int value >= 1. `checkSpeed <#checkspeed>`__ will return
   true when ``(frameCount % speed)`` equals 0, making this an inverse
   value. Lower is faster. 1 means `checkSpeed <#checkspeed>`__ will
   return True *every* frame. 4 means `checkSpeed <#checkspeed>`__
   returns True every *fourth* frame and is 1/4th the speed.

addKeyFunc
^^^^^^^^^^

(key, func, speed=1, hold=True)

-  **key** - Name of the key used by your
   [[GamePad\|GamePad#class-basegamepad]] instance, such as "A" or
   "START"
-  **func** - Function to call when key is pressed or held. May be a
   lambda.
-  **speed** - How often to respond to the key being pressed. Same logic
   as `checkSpeed <#checkspeed>`__.
-  **hold** - Continue to call func as long as the key is pressed.

handleKeys
^^^^^^^^^^

This **MUST** be called inside of the animation `step() <#step>`__
method. It is kept as a manual call so that the developer can decide
where in their `step() <#step>`__ process to handle inputs.

Class *BaseCircleAnim*
----------------------

BaseCircleAnim is the basis for any animation that runs with an instance
of [[Circle]] and provides all the same methods and properties as
`BaseAnimation <#class-baseanimation>`__ plus those below.

\_\_init\_\_
^^^^^^^^^^^^

(layout)

-  **layout** - An instance of [[Circle]]

Note: The start and end parameters must be respected by the inheriting
animation for them to do anything.

Properties
~~~~~~~~~~

--------------

In addition to the properties provided by
`BaseAnimation <#class-baseanimation>`__, the following properties are
available to classes that inherit from
`BaseCircleAnim <#class-BaseCircleAnim>`__.

rings
^^^^^

Array of the ring mapping provided to the [[Circle]] instance.

ringCount
^^^^^^^^^

Total number of rings, as passed to the [[Circle]] instance.

lastRing
^^^^^^^^

Index of the outer most ring on the circle.

ringSteps
^^^^^^^^^

Array of degrees between each pixel for the given ring index.

Class *Sequence*
----------------

``Sequence`` automatically handles stepping through queues of animations
while being an animation itself, making it very easy to integrate into
existing code. It provides all the same methods available on
[[BaseAnimation]].

\_\_init\_\_
^^^^^^^^^^^^

(layout, animations=None)

-  **layout** - An instance of [[Layout]]
-  **animations** - A list of animation class objects to run, can be of
   any type. If none are given they must be added with
   `addAnim <#addanim>`__ before calling run().

add\_animation
^^^^^^^^^^^^^^

(anim, amt = 1, fps=None, max\_steps = 0, untilComplete = False,
max\_cycles = 0)

-  **anim** - Animation class object to add to internal queue
-  **amt** - Same as amt parameter on the `step() <#step>`__ method.
-  **fps** - Framerate to run animation at. If left as None, the
   framerate given when calling Sequence.run() will be used, allowing
   for a default framerate across all animations in the queue.

All other parameters are the same as on the base animation
`run() <#run>`__ method but you *must* use either max\_steps or
untilComplete and max\_cycles, otherwise the animation with run forever
and later animations will never be run!
