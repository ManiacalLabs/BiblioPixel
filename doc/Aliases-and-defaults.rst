All this can amount to a lot of typing, so BiblioPixel gives you some
shortcuts.

Typename expansion.
-------------------

If you are only specifying a ``typename`` for a component, then you
don't have to specify the entire dictionary, just the name of the class.

This means that a project

::

    {"driver": {"typename": "bibliopixel.drivers.API.LPD8806.LPD8806"}}

is identical to the easier-to-read

::

    {"driver": "bibliopixel.drivers.API.LPD8806.LPD8806"}

Aliases.
--------

Aliases are just shorthand for some common classes. It lets you write
the project

::

    {"driver": "bibliopixel.drivers.API.LPD8806.LPD8806"}

as

::

    {"driver": "LPD8806"}

You can find a current list list of the aliases in `this
file <https://github.com/ManiacalLabs/BiblioPixel/blob/master/bibliopixel/project/aliases.py>`__.

Aliases are case insensitive.

Command-line flags.
-------------------

There are three command line flags that are used to fill in missing
components in your project file - ``--driver``, ``--layout``, and
``--animation``.

You can either pass in an alias, or for more control, a JSON dictionary,
which you will have to quote for your shell:

::

    bibliopixel --animation=matrix_test
    bibliopixel --layout='{"typename": "matrix", "width": 12, "height": 12}'

The ``--ledtype`` command line flag.
------------------------------------

The [[SPI]] and [[Serial]] drivers require an ``"ledtype"`` field to
identify the hardware type of the LED - see `LED
Types <Serial#led-types>`__. You can use the ``--ledtype`` flag to enter
this value from the command line as either a string or an integer.
