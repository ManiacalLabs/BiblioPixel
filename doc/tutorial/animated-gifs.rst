About the animated GIFs
---------------------------

Those pretty pictures are automatically generated from the example BiblioPixel
projects embedded in the documentation, so they fairly faithfully represent the
results you would get.

The one big difference is that that the GIFs loop after ten seconds (to keep
their size down), where the real animation will keep playing forever.

They're embedded in the text as examples of how to make Projects, and there's
also a unique one at the bottom of each page just for fun, as a sort of gallery
of animations.

You can generate your own animated GIFs from your Projects - see
`here <topic-papers/writing-animated-gifs>`_ .

----

.. code-block:: yaml

   shape: [64, 16]
   animation:
     typename: $bpa.matrix.Twinkle
     speed: 5
     density: 100

.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/0-footer.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/0-footer.gif
   :alt: Result
   :align: center
