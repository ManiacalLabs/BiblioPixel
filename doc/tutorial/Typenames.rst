Typenames
------------------------

What is a Typename?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

BiblioPixel lets you load projects, parts of projects, or even Python code from
your local drive or from the Internet, and Typenames are BiblioPixel's way of
identifying what code that is.

A *Typename* names a Python class.  Typenames appear in Class Sections only -
i.e. ``animation``\ , ``controls``\ , ``drivers``\
, or ``layout``\.

Examples of Typenames are:

* ``BiblioPixel.animation.fill.Fill``
* ``.sequence``
* ``BiblioPixelAnimations.strip.PartyMode.PartyMode``
* ``$bpa.strip.PartyMode``

For easier reading and writing of Projects, if a Class Section is a string
instead of a dictionary, that string used as the ``typename`` - so these two
projects mean the same:

.. code-block:: yaml

     animation:
       typename: .sequence


.. code-block:: yaml

     animation: .sequence

.. bp-code-block:: footer

   shape: [96, 8]
   animation:
     typename: $bpa.strip.Wave
     color: coral
