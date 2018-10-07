The BiblioPixel Tutorial
------------------------------

The tutorial steps you through all the features of BiblioPixel, starting with
creating a project and going onto advanced topics like controls.

.. toctree::
   :maxdepth: 1

   tutorial/Before-you-start
   tutorial/Installing-BiblioPixel
   tutorial/How-to-write-a-Project
   tutorial/The-bp-program
   tutorial/Projects
   tutorial/The-animation-Section
   tutorial/The-run-Section
   tutorial/The-shape-and-layout-Sections
   tutorial/Typenames
   tutorial/Palettes
   tutorial/The-path-and-aliases-Sections
   tutorial/The-driver-and-drivers-Sections
   tutorial/The-Serial-Driver
   tutorial/The-controls-Section
   tutorial/Routing-Addresses-and-Actions

-------

.. code-block:: yaml

   shape: [64, 7]
   animation:
     typename: $bpa.matrix.Text.ScrollText
     text: 'BiblioPixel Tutorial'

.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial.gif
   :alt: Result
