Yaml or JSON: how BiblioPixel stores its data
--------------------------------------------------

BiblioPixel represents lighting Projects as text files in one of two formats -
`YAML <https://github.com/darvid/trine/wiki/YAML-Primer>`_
or `JSON <https://json.org>`_\ .  If you know about these formats, you can skip
ahead to the next page.

Most of our examples are in YAML, because it's less typing - however, many
people who write Javascript prefer JSON and that works perfectly well too.

BiblioPixel doesn't care about which file names you use, but it's neater to put
JSON data in files ending in .json and YAML data in files ending in .yml.

You can learn YAML by example, from reading this document.  If you're interested
in a bit more information, here's
`a link <https://github.com/darvid/trine/wiki/YAML-Primer>`_\ .

**Example 1**\ : Some data in JSON:

.. bp-code-block:: example-1

    {
        "animation": {
            "typename": "sequence",
            "length": 3,
            "animations": [
                ".tests.PixelTester",
                {
                    "typename": "fill",
                    "color": "red"
                },
                "$bpa.matrix.MatrixRain"
            ]
        },
        "shape": [32, 12]
    }


**Example 2**\ :  The same data in YAML:

.. bp-code-block:: example-2

   animation:
     # Run three different animations, each for three seconds.
     typename: sequence
     length: 3

     animations:
       - .tests.PixelTester
       - typename: fill
         color: red
       - $bpa.matrix.MatrixRain

   shape: [32, 12]

YAML isn't just shorter and cleaner: it lets you write comments to yourself or
anyone else reading, by starting a line with the ``#`` character.

We make heavy use of this "comment" feature in our own projects, and we suggest
you do too when writing yours, unless your memory is better than ours.

.. bp-code-block:: footer

   shape: [64, 16]
   animation:
     typename: $bpa.matrix.MathFunc
     func: 23
     palette:
       colors: eight
       continuous: true
       scale: 0.01
