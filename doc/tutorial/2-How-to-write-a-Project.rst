
2. How to write a Project
=========================

This section will guide you throw creating a new project from scratch, and
editing it to make tiny changes.


1. Open a command line
^^^^^^^^^^^^^^^^^^^^^^^^^^^

2. Change directory to the directory you want to work in
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Often you'd want to work in your home directory:

.. code-block:: bash

   cd ~

3. Use the ``bp new <your-project-name>`` to create a new project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   bp new my_lights

This will create a new directory named ``my_lights/`` in your current directory.

That directory contains a sample project file and a sample Python file for you
to edit.

4. Run the Project file:
^^^^^^^^^^^^^^^^^^^^^^^^

Change directory to the project directory, and run the Project file, like this:

.. code-block:: bash

   cd my_lights
   bp -s my_lights.yml

.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-1.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-1.gif
   :alt: Result

The ``-s`` flag to ``bp`` means "open a SimPixel window" and it will indeed open
on your browser, showing a lighting pattern like the one above.


5.  Stop the program.
^^^^^^^^^^^^^^^^^^^^^

Press Control-C to stop the ``bp`` program. Close the browser window.


6. Edit the Project to change the Shape.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

With your text editor, edit the project file ``my_lights.yml``.

Go to the line that says: ``shape: [32, 48]`` and change it to say
``shape: [96, 16]`` and run the Project again.  You should see this:


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-2.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-2.gif
   :alt: Result


Now change that line to say: ``shape: [48, 48]`` and run the Project again.  You
should see this:


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-3.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-3.gif
   :alt: Result


7. Change the Animation
^^^^^^^^^^^^^^^^^^^^^^^

Go to the line that says: ``animation: $bpa.matrix.bloom`` and change it to say
``animation: $bpa.matrix.SpinningTriangle`` and run it again.  You get this:


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-4.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-4.gif
   :alt: Result


Now, let's try a sequence.

Delete that line ``animation: $bpa.SpinningTriangle``

Go down a little to around line 48, and uncomment all those lines by removing
the first *two* characters from each line, so it looks like this:

.. code-block:: yaml

   animation:
     typename: sequence
     length: 2
     animations:
       - $bpa.bloom
       - $bpa.pinwheel
       - $bpa.GameOfLife.GameOfLifeRGB
       - $bpa.SpinningTriangle

Run it again.  You should see a series of four animations, each running for ten
seconds, like this:


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-5.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-5.gif
   :alt: Result


8.  Use a custom Python Animation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``bp new`` command creates a new custom Python animation for you to play with.
In this case, it's called ``my_lights.MyLights``.

Delete the ``animation:`` lines above with the ``sequence``\ , scroll down a
little to the lines at the end of the Project file, and uncomment them:

.. code-block:: yaml

   animation:
     typename: my_lights.MyLights
     color: red

Resulting in this:


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-6.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-6.gif
   :alt: Result


Run the Project again.  Change the ``color:`` line to read ``color: goldenrod`` and
run it again to get this:


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-7.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-7.gif
   :alt: Result


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


----

.. code-block:: yaml

   shape: [64, 16]
   animation: $bpa.matrix.GameOfLife.GameOfLifeRGB


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-footer.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-footer.gif
   :alt: Result
