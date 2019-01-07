Editing a Project
-----------------------------

On this page, you edit the project you created on the previous page.


1. Edit the Project to change the Shape.
========================================

With your text editor, edit the project file ``my_lights.yml``.

Go to the line that says: ``shape: [32, 48]`` and change it to say
``shape: [96, 16]`` and run the Project again.  You should see this:


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-2.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-2.gif
   :alt: Result
   :align: center


Press control-c to stop the ``bp`` program when you're ready to move on - you'll
need to do this for each step on this page.

Now change that line to say: ``shape: [48, 24]`` and run the Project again.  You
should see this:


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-3.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-3.gif
   :alt: Result
   :align: center


2. Change the Animation
=========================

Go to the line that says: ``animation: $bpa.matrix.bloom`` and change it to say
``animation: $bpa.matrix.SpinningTriangle`` and run it again.  You get this:


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-4.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-4.gif
   :alt: Result
   :align: center


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
   :align: center
