The ``aliases`` and ``path`` Sections
=================================================

The optional ``path`` and ``aliases`` Sections make it easier for you to find
Python code for Typenames.


The ``aliases`` Project Section.
------------------------------------

The optional Project Section ``alias`` is a dictionary of aliases to Typenames
or parts of Typenames that can be put together to save typing in your project.

Either the ``$`` or the ``@`` character can used interchangeably to introduce an
alias into a typename.

Aliases are terminated by the characters ``.``\ , ``/`` or ``#``.

There is one alias built in: ``$bpa`` maps to ``BiblioPixelAnimations``.

**Example 1**\ : Using ``aliases``

.. code-block:: yaml

       aliases:
         mat: BiblioPixelAnimations.matrix
         fade: christmas_lights.Fade

       animation:
           typename: sequence
           length: 2
           animations: [$mat.ImageAnim, $fade, $mat.ImageShow, $fade]

The ``path`` Project Section.
---------------------------------

The optional Project Section ``path`` is a list of external directories that
contain extra Python code used by the Project.

The ``path`` is represented either by a list of strings, or by a single string
which is a list of directories separated by colons (like the ``PATH`` and
``PYTHONPATH`` environment variables).

When Typenames in a Project are resolved to a class, these directories are
searched for code, in this order:


#. The local directory
#. The directory local to the Project .json file
#. Directories in the  ``path`` Project Section, in order given in the project
#. Directories in the ``PYTHONPATH`` environment variable
#. The Python installation directory


**Example 2**\ : Using ``path``

.. code-block:: yaml

       path: [/home/pi/my-library, /var/stuff/some-library]

       # Equivalent using colon separated strings would be
       # path: "/home/pi/my-library:/var/stuff/some-library"


----

.. code-block:: yaml

   shape: [96, 8]
   animation: $bpa.strip.Rainbows.Rainbow


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/the-path-and-aliases-sections-footer.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/the-path-and-aliases-sections-footer.gif
   :alt: Result
   :align: center
