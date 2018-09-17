
.. code-block:: yaml

   shape: [32, 48]
   animation: $bpa.matrix.bloom


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-1.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-1.gif
   :alt: Result


.. code-block:: yaml

   shape: [96, 16]
   animation: $bpa.matrix.bloom


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-2.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-2.gif
   :alt: Result


.. code-block:: yaml

   shape: [48, 48]
   animation: $bpa.matrix.bloom


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-3.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-3.gif
   :alt: Result


.. code-block:: yaml

   shape: [48, 48]
   animation: $bpa.matrix.SpinningTriangle


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-4.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-4.gif
   :alt: Result


.. code-block:: yaml

   shape: [48, 48]

   animation:
     typename: sequence
     length: 2
     animations:
       - $bpa.matrix.bloom
       - $bpa.matrix.pinwheel
       - $bpa.matrix.GameOfLife.GameOfLifeRGB
       - $bpa.matrix.SpinningTriangle


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-5.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-5.gif
   :alt: Result


.. code-block:: yaml

   shape: [48, 48]

   animation:
     typename: test.bibliopixel.animation.documentation_class.Example26
     color: red


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-6.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-6.gif
   :alt: Result


.. code-block:: yaml

   shape: [48, 48]

   animation:
     typename: test.bibliopixel.animation.documentation_class.Example26
     color: goldenrod


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-7.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-7.gif
   :alt: Result


.. code-block:: yaml

   shape: [48, 48]

   animation:
     typename: test.bibliopixel.animation.documentation_class.Example28
     color: goldenrod


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-8.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/2-example-8.gif
   :alt: Result
