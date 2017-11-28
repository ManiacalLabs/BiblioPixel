The ``bibliopixel`` command line program.
=========================================

The program ``bibliopixel`` is the command line front end to
BiblioPixel, the LED control system.

You can use ``bibliopixel`` to run demos or your own projects, to set
and get defaults for projects, or to discover hardware devices attached
to your computer.

Basic usage of ``bibliopixel``.
-------------------------------

The ``bibliopixel`` program is installed automatically when the
BiblioPixel system is installed and can be executed from the command
line by typing ``bibliopixel <command>`` and hitting return.

The possible commands at this writing are ``all_pixel``, ``devices``,
``demo``, ``help``, and ``run`` and they fit into four categories:

-  `Project <Project-Commands>`__: ``bibliopixel run`` runs BiblioPixel
   projects.

-  `Demo <Demo-Commands>`__: ``bibliopixel demo`` runs premade demos in
   your browser.

-  `Hardware <Hardware-Commands>`__: ``bibliopixel all_pixel`` and
   ``bibliopixel devices`` discover and list devices.

-  `Help <Help-Command>`__: ``bibliopixel help`` gives detailed
   instructions for each command.

You can load Python libraries dynamically from disk or public git
repositories - see [[BiblioPixel Paths]] for more information.

Command line flags for ``bibliopixel``
--------------------------------------

All the flags for the ``bibliopixel`` command have to come at the end of
the command line - like this:

::

     bibliopixel demo  bloom --loglevel=info --numpy --verbose

Common flags for all commands:

::

    -h, --help            show this help message and exit
    --loglevel {debug,info,warning,error,critical}
                          Set what level of events to log. Higher log
                          levels print less.
    --path PATH           A list of directories, separated by colons,
                          'which are added to the end of `sys.path`. You
                          can also use gitty-style paths which start with
                          `//git/` to dynamically load a library from a
                          public git repository. See
                          https://github.com/ManiacalLabs/BiblioPixel/wiki
                          /BiblioPixel-Paths for more information.

--------------

Flags for ``run`` and ``demo`` commands.

::

    -d DRIVER, --driver DRIVER
                          Default driver type if no driver is specified
    -l LED, --layout LAYOUT     Default LAYOUT class if no LAYOUT is specified
    -t LEDTYPE, --ledtype LEDTYPE
                          Default LED type if no LED type is specified
    -a ANIMATION, --animation ANIMATION
                          Default animation type if no animation is
                          specified

--------------

Flags for the ``run`` command only.

::

    -j, --json            Enter JSON directly as a command line argument.

--------------

Flags for the ``demo`` command only.

::

    --width WIDTH         X dimension of display
    --height HEIGHT       Y dimension of display
    --depth DEPTH         Z dimension of display. Only used for Cube
                          demos.
    --simpixel SIMPIXEL   URL for SimPixel program.

--------------

Flags for the ``all_pixel`` and ``devices`` commands.

::

    --hardware-id HARDWARE_ID
                          USB Vendor ID : Product ID of device. Defaults
                          to VID:PID for AllPixel
    --baud BAUD           Serial baud rate.
