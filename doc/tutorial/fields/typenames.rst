The ``typename`` Field identifies a Python class.
---------------------------------------------------

BiblioPixel lets you load projects, parts of projects, or even Python code from
your local drive or from the Internet.  The ``typename`` Field is BiblioPixel's
way of identifying what code that is.

Typenames appear in Class Sections only - i.e. ``animation``, ``controls``,
``driver``, ``drivers``, or ``layout``.

**Examples**:

* ``BiblioPixel.animation.fill.Fill``
* ``.sequence``
* ``BiblioPixelAnimations.strip.PartyMode.PartyMode``
* ``$bpa.strip.PartyMode``

In the last example, a special Alias ``$bpa`` is short for
``BiblioPixelAnimations``.

For easier reading and writing of Projects, if a Class Section is just a string,
that string used as the ``typename`` - so these two projects mean the same thing:

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
