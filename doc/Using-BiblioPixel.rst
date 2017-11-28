There was only one way to use BiblioPixel before 3.0: you wrote a Python
program which created a ``Device``, an ``LED`` and one or more
``Animations`` and then run those animations.

BiblioPixel 3.0 introduces *Projects*, which do the same thing in data,
so you can run BiblioPixel without ever writing Python programs.

A Project is just a `JSON <http://json.org>`__ file with five parts:
``driver``, ``layout``, ``animation``, ``run``, ``path``.

Writing your own programs is still completely supported, and your
existing BiblioPixel programs from before 3.0 will run with at worst
tiny changes but perhaps none at all. However, we believe it should also
be very easy to port your working project into a Project, and you get a
lot of really useful features, like dynamic loading of other people's
libraries right from github and gitlab - please email us at
bibliopixel-users@googlegroups.com for help.
