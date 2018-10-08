The ``run`` section
-----------------------------

The Value Section ``run`` is a dictionary with the following Fields:

``fps`` (default ``0``\ )
  Maximum number of frames per second to display

``max_cycles`` (default ``0``\ )
  If set, play the animation this many times.
  If ``max_cycles`` is ``0``\ , then play the animation forever.

``seconds`` (default ``None``\ )
  Maximum number of seconds to play, if set.

For developers only, there's one more field:

``main`` (default ``None``\ )
  If non-empty, then ``bp`` runs in a background
  thread, and the function named here runs in the foreground


Examples
========

**Example 1**\ :  Run forever at 30 frames per second (fps)

.. code-block:: yaml

   run:
     fps: 30

**Example 2**\ :  Run for two seconds at 10 fps

.. code-block:: yaml

   run:
     seconds: 2
     fps: 10

**Example 3**\ :  Run three times

.. code-block:: yaml

   run:
     max_cycles: 3

----

.. code-block:: yaml

   shape: [64, 17]
   animation: $bpa.matrix.circlepop


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/6-footer.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/6-footer.gif
   :alt: Result
   :align: center
