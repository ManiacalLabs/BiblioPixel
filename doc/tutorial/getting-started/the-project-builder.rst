The Project Builder
------------------------

The Project Builder is a Python class lets you use Projects and write your own
main program in Python, or experiment in the Python interpreter


How to use the Project Builder from the Python interpreter
================================================================================

Using the Project Builder from the Python interpreter is a lot of fun, and
anything you do there can be cut-and-pasted into your own scripts.

There's automatically generated class documentation here[TODO], but the
walkthrough below will probably be more entertaining.

.. code-block:: python

    $ python3

    from bibliopixel.project.builder import Builder
    pb = Builder()
    print(pb)
    # Nothing in it yet...

    # Open a simpixel in your browser.
    pb.simpixel()

    # Let's start it!
    pb.start()
    # You're starting an empty project, which works perfectly well but does nothing.
    # Hit Control-C to stop it

    pb.shape = 12
    pb.animation = '.tests.PixelTester'
    # This resolves to bibliopixel.animation.tests.PixelTester

    pb.start()
    # Now you should see stuff!
    # This blocks - you don't get a Python prompt while it's running.
    # Hit Control-C to stop it

    # Let's run in the background, like this:
    pb.threaded = True
    pb.start()
    # Now you can keep going!

    pb.shape = 128
    pb.animation = '$bpa.strip.Wave'
    # Resolves to BiblioPixelAnimations.strip.Wave.Wave

    # Restart the project with the changes
    pb.start()
    print(pb)

    pb.save('test.yml')  # Save the data in a file

    dr = Builder()       # Let's make a new project, just for driver info
    dr.driver = '.serial.driver.Serial'
    dr.driver.update(c_order='RGB', device_id=10)

    dr.start()

    dr.running_builder.stop()  #

    dr.save('driver.yml')  # I'm going to merge it into

    print(pb)
    driver: {c_order: RGB, device_id: 10, typename: .serial.driver.Serial}

    (pb + dr).start()  # Restarts the Project with a new driver
