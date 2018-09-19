BiblioPixel - the light programming system
----------------------------------------------

BiblioPixel is a free, open-source Python program for creating and sharing
light sequences and animations, particularly for LED strips.

In one sentence:
=====================

Animate complex lighting projects by writing simple text files.

.. code-block:: yaml

    animation:
      typename: $bpa.matrix.MathFunc
      func: 1
      rand: false

    shape: [64, 64]


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/index.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/index.gif
   :alt: Result


Features
============


BiblioPixel has some snappy features:


* It runs on the Raspberry Pi, Windows, MacOS and Linux.

* It has drivers for almost every popular LED strip, and many other lights.

* Lighting projects can be put together without any programming...

* ...and it's easy to reuse projects...

* ...but if you program, it's also easy to write your own Animations, Controls,
  Drivers and Layouts in Python.

* There's a fast and free `WebGL visualizer <http://simpixel.io>`_ driver,

* ...and a REST Control...

* ...and you can also make animated GIFs to send to your friends.

* BiblioPixel uses high-performance `numpy <http://www.numpy.org/>`_
  arithmetic...

* ...but plays nicely with plain old Python lists (and classic BiblioPixel
  code).

* There are Controls like REST, MIDI and keyboard that can control any
  animation, layout, device or other control – also without programming.

* ...and much more.


.. toctree::
   :maxdepth: 2
   :hidden:

   documentation

-------------------------------

.. code-block:: yaml

   animation: $bpa.strip.Wave
   shape: [64, 11]

.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/index-footer.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/index-footer.gif
   :alt: Result
