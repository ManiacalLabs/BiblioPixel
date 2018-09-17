13. Routing, Addresses and Actions

A routing example
^^^^^^^

Now you have Messages coming in, you need to tell the Control where to send
them, by filling out a ``routing`` dictionary in the Project.

Make sure your MIDI controller is working by using ``bp monitor midi`` as in the
previous section.

Now download and run `this project <midi-1.yml>`_ with ``bp -s midi-1.yml`` and
move the first four faders around.  You should see the four different animations
fade in and out as you move the faders around.

**Example 1**\ : A MIDI control project

.. code-block:: yaml

   shape: 50

   animation:
     typename: mixer
     levels: [1, 0, 0, 0]
     animations:
       - $bpa.strip.Rainbows.RainbowCycle
       - $bpa.strip.Wave
       - $bpa.strip.HalvesRainbow
       - $bpa.strip.PartyMode

   controls:
     typename: midi
     routing:
       control_change:
         0: animation.levels[0]
         1: animation.levels[1]
         2: animation.levels[2]
         3: animation.levels[3]


 --------------------------

.. code-block:: yaml

   shape: [64, 24]
   animation:
     typename: $bpa.matrix.MathFunc
     rand: False
     func: 12


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/12-footer.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/12-footer.gif
   :alt: Result
