Using `numpy` color lists
-----------------------------------

Introduction
====================

All BiblioPixel animation is accomplished by changing a *color list* - a list of RGB
colors.

In all BiblioPixel versions up until and including v3, a color list was a Python list
of Python tuples.

We call this "classic Python lists". This was very convenient and easy to
understand - but classic lists are slow and uses a lot of memory if there are a
lot of colors, and even quite simple operations on classic lists require
many lines of code.

Enter ``numpy``\ !

``numpy`` <http://www.numpy.org/>`_ is a Python package that has purely numeric
arrays (lists and matrices) that use less memory and are a lot faster - but even
better, ``numpy`` also lets you express even quite complex numeric operations with
a smaller amount of clearer code than using classic lists.

Since BiblioPixel version 3.4.0, animations can use ``numpy`` arrays by setting the
Project section `"numbers"` to be `"float32"`.

Starting in BiblioPixel 4.0, ``numpy`` arrays will be the default, and fairly
soon after that, we'll be phasing out classic lists.

What's a ``numpy`` color list like?
---------------------------------------

Whether it's ``numpy`` or "classic", a color list is just a list of RGB colors.

Almost all operations that work on a classic list work the same way on a ``numpy``
list: for example:

.. code-block:: python

       from bibliopixel.project.data_maker import ColorList, NumpyColorList
       from bibliopixel.util.colors import COLORS

       classic_list = ColorList(4)
       numpy_list = NumpyColorList(4)

       classic[0] = COLORS.yellow
       classic[1:4] = COLORS.red, COLORS.green, COLORS.blue

       numpy_list[0] = COLORS.yellow
       numpy_list[1:4] = COLORS.red, COLORS.green, COLORS.blue

sets the first four colors of a color list to yellow, red, green and blue.

Unlike classic lists, you can write over components in a color_list:

.. code-block:: python

       numpy_list[0][0] = 0
       # classic_list[0][0] = 0    # Can't modify a tuple!  throws a TypeError.

Where ``numpy`` disinguishes itself is operations that apply to all the colors at
once.  To reduce the intensity of each color just created by 50%:

.. code-block:: python

       for i, (r, g, b) in enumerate(classic):
           classic[i] = (r / 2, g / 2, b / 2)

        # Much easier:
        numpy_list /= 2

It works even better if you have multiple lists - you can do slick things like:
`numpy_list = (2 * list_1 + 3 * list_2) ** 2.5`

Be careful:  references can be tricky
-------------------------------------

Unlike classic lists, if you extract a color from a ``numpy`` color list and then
modify it, the original list is also changed!

.. code-block:: python

       numpy_list[:] = COLORS.red, COLORS.green, COLORS.blue

       color = numpy_list[0]

       # later
       color[0] = 0

       numpy_list[0]  # Now it's black!

How to get your BiblioPixel Animation to use ``numpy`` lists.
-----------------------------------------------------------------

You won't need to change anything in your Project at all, but if you have
written a custom Animation, you might need to change your code.

In our experience so far, 95% of existing Animations worked immediately with
``numpy`` and all the rest required only tiny changes.

You can easily find out - just run your project with the command line float
`--numbers=float` like this:

.. code-block:: python

       bp --numbers=float your-project-name.json

If there's an error, contact us at
`Maniacal Labs Users <mailto:maniacal-labs-users@googlegroups.com>`_
and send us the code for your Animation and the error!
