BiblioPixel would be useless if new animations couldn't easily be added.
While you don't *need* do use the animation classes to produce an
animation effect, doing so will greatly ease the process in most cases.

The [[BaseStripAnim\|Animations#class-basestripanim]] and
[[BaseMatrixAnim\|Animations#class-basematrixanim]] classes work around
the concept of generating an animation as a simple state machine, where
each frame of the animation is generated in an atomic operation.

For example, the following strip animation class:

.. code:: python

    class StripTest(BaseStripAnim):
        def __init__(self, led, start=0, end=-1):
            #The base class MUST be initialized by calling super like this
            super(StripTest, self).__init__(led, start, end)
            #Create a color array to use in the animation
            self._colors = [colors.Red, colors.Orange, colors.Yellow, colors.Green, colors.Blue, colors.Indigo]

        def step(self, amt = 1):
            #Fill the strip, with each sucessive color
            for i in range(self._led.numLEDs):
                self._led.set(i, self._colors[(self._step + i) % len(self._colors)])
            #Increment the internal step by the given amount
            self._step += amt

[[img/strip\_test.gif]]

This animation displays successive colors from self.\_colors every time
[[step()\|Animations#stepamt--1]] is called. At the end of the call to
[[step()\|Animations#stepamt--1]], [[self.\_step\|Animations#\_step]] is
incremented by *amt*. If the animation does not require keeping track of
the current step, this can be omitted, but it must be implemented if
needed by the animation. This is all that is required for any animation,
refer to [[BaseStripAnim\|Animations#class-basestripanim]] for more
information on other available methods and properties.

Creating a matrix animation is not much different:

.. code:: python

    class MatrixTest(BaseMatrixAnim):
        def __init__(self, led):
            #The base class MUST be initialized by calling super like this
            super(MatrixTest, self).__init__(led)
            #Create a color array to use in the animation
            self._colors = [colors.Red, colors.Orange, colors.Yellow, colors.Green, colors.Blue, colors.Indigo]

        def step(self, amt = 1):
            #Fill the strip, with each sucessive color
            for i in range(self._led.numLEDs):
                self._led.drawRect(-1, -1, i+1, i+1, self._colors[(self._step + i) % len(self._colors)])
            #Increment the internal step by the given amount
            self._step += amt

[[img/matrix\_test.gif]]

As you can see, the basics are no different other than
[[self.\_led\|Animations#\_led]] is an [[Matrix]] instance instead of
[[Strip]], so matrix functions like
[[drawRect\|Matrix#drawrectx-y-w-h-color]] are available for use.

The [[update()\|Layout#update]] method of [[Layout]] ***must not*** be
called from inside the [[step()\|Animations#stepamt--1]] method as it
will automatically be called by
[[run()\|Animations#runamt--1-fpsnone-sleepnone-max\_steps--0-untilcomplete--false-max\_cycles--0]].
