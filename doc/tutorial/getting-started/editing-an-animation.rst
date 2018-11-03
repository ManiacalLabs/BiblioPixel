Editing a custom animation
-----------------------------

You're continuing to edit the Project from the last two pages.

1.  Use a custom Python Animation
=================================

The ``bp new`` command creates a new custom Python animation for you to play
with.  In this case, it's called ``my_lights.MyLights``.

Delete the ``animation:`` lines above with the ``sequence``, scroll down a
little to the lines at the end of the Project file, and uncomment them:

.. code-block:: yaml

   animation:
     typename: my_lights.MyLights
     color: red

Resulting in this:


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-6.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-6.gif
   :alt: Result
   :align: center


Run the Project again.  Change the ``color:`` line to read ``color: goldenrod``
and run it again to get this:


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-7.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-7.gif
   :alt: Result
   :align: center


2. Editing a Python Animation
=================================

Now let's change the Python code.

With your text editor, edit the Python file ``my_lights.py``.

After these lines in the file:

.. code-block:: python

    # Set the previous pixel to black.
    self.color_list[this_pixel - 1] = COLORS.black

add these two lines:

.. code-block:: python

    self.color_list[this_pixel - 2] = COLORS.yellow
    self.color_list[this_pixel - 3] = COLORS.black

and run it again to get this:

.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-8.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-8.gif
   :alt: Result
   :align: center


.. bp-code-block:: footer

   shape: [64, 16]
   animation: $bpa.matrix.GameOfLife.GameOfLifeRGB
