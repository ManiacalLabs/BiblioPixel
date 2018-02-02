:orphan:

Welcome to BiblioPixel
======================

BiblioPixel is a pure Python 3 library for all your LED animations
needs. Through its fully output agnostic design you can write your code
once and use it on a huge variety of outputs, from LED strips to cubes
and even a high performance LED simulator!

BiblioPixel allows many different display geometries. Many of the
existing hardware models are LED strips, matrixes or circles, but there
are no real limits on what the output device can be, due to the output
:doc:`Drivers <Drivers>` model.

User Guide
----------

.. toctree::
   :maxdepth: 2

   Porting-from-2.x-to-3.x
   Installation
   Display-Setup
   SPI-Setup
   The-bp-Command

API Reference
-------------

.. toctree::
    :maxdepth: 1
    :glob:

    api/*

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
