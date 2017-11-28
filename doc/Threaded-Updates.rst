As of v1.1.0 of BiblioPixel, there is support for pushing data to the
display on a background thread. In many cases, this can vastly increase
the maximum frame rate at which the display can be updated. This is
because the next animation frame can be generated while the display is
updated, instead of waiting for the update to finish.

Threaded updates defaults to off and it is best to test with the feature
both on and off before settling on which to use. It can be enabled by
setting the threadedUpdate parameter to True, like this:

.. code:: python

    led = Strip(driver, threadedUpdate = True)

Depending on the display, operating system, CPU capabilities, and if
multiple devices are being used, not using threaded updates may even be
faster. For example, on a single CPU core system like the Raspberry Pi,
the update thread must share CPU time with the frame generation thread.
So there is little advantage. But on a multi-core CPU system, the
generation thread and update thread(s) will likely run on different
cores, therefore not sharing system resources.

If the frame takes less time to be generated then the display takes to
update, have no fear. When the [[Strip]] or [[Matrix]] update() method
is called, it will wait until previous updates finish. So, if the
display requires 20ms to update and the frame takes 10ms to generate,
the next update call will return after the remainder, around 10ms. This
still speeds everything up since, otherwise, it would require 10ms for
frame generation *plus* 20ms for update, for a total of 30ms per frame,
instead of 20ms. Since display update takes longer than frame
generation, that part is effectively free, from a time perspective.
