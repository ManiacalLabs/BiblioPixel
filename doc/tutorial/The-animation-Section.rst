The ``animation`` Section
================================

BiblioPixel comes with a library of Animations called BiblioPixelAnimations
which you can reuse without programming.

And if you can program, writing an Animation is quite easy and often the best
way to solve your problem - there are more types of Animation than all the other
class types put together.

The ``animation`` Class Section complements with the ``run`` Value Section.

The ``animation`` Section describes a specific program that dynamically changes
the lights over time, while the ``run`` Section describes more general
information - like the frame rate (in frames per second or fps), or how many
times the whole Animation is repeated.


The Fields in the ``animation`` Section depend on its Class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Aside from ``typename``\ , the Fields in the ``animation`` Section depend
entirely on the Class of the Animation itself (which is true for every Class
Section).

Each Animation Class has a documentation page which should explain how it works,
lists its Fields, and give examples of usage.


**Example 1**\ : a single Animation with no Fields

.. code-block:: yaml

   animation: $bpa.matrix.bloom
   shape: [32, 32]


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/5-example-1.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/5-example-1.gif
   :alt: Result
   :align: center


**Example 2**\ : an animation with fields ``scroll``\ , ``color`` and ``bgcolor``

.. code-block:: yaml

   animation:
     typename: $bpa.matrix.Mainframe
     scroll: false
     color: green
     bgcolor: dark gray

   shape: [32, 32]


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/5-example-2.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/5-example-2.gif
   :alt: Result
   :align: center


**Example 3**\ : Mix four animations together

.. code-block:: yaml

   animation:
       typename: mixer
       levels: [0.25, 0.25, 0.25, 0.25]
       animations:
           - $bpa.matrix.ImageAnim
           - $bpa.matrix.ImageShow
           - $bpa.matrix.ImageDissolve
           - $bpa.matrix.Mainframe

   shape: [64, 64]


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/5-example-3.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/5-example-3.gif
   :alt: Result
   :align: center


Listing the Animation Classes.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To get a list of the ``typenames`` for Animation Classes that are bundled with
BiblioPixel, use the ``bp animations`` Command:

.. code-block:: bash

   $ bp animations

   circle:
     $bpa.circle.Twinkle
     $bpa.circle.arc_clock
     [... many more ...]

   collection:
     .split

   cube:
     $bpa.cube.GameOfLife.CubeGameOfLife
     $bpa.cube.Rain.RainBow
     $bpa.cube.bloom.CubeBloom

   [... many more ...]

----

.. code-block:: yaml

   shape: [64, 17]
   animation: $bpa.matrix.pinwheel


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/5-footer.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/5-footer.gif
   :alt: Result
   :align: center
