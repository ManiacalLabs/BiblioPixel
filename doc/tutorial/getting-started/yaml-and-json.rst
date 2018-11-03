Yaml and JSON
--------------------------------------------------

A Lighting Project is a JSON or Yaml file.

* `JSON <https://json.org>`_ files end in .json
* `Yaml <https://github.com/darvid/trine/wiki/YAML-Primer>`_ files end in .yml

Examples are mostly in Yaml, a minimal format that's backward-compatible with
JSON.

**Example 1**: Some data in JSON:

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


**Example 2**:  The same data in YAML:

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

----

YAML lets you write helpful comments for yourself or anyone else reading, by
starting a line with the ``#`` character:

.. bp-code-block:: footer

   shape: [64, 16]
   animation:
     typename: $bpa.matrix.MathFunc
     func: 23
     palette:
       colors: eight
       continuous: true
       scale: 0.01  # Gentle soft ripppling colors
       # scale: 100   # Psycho strobe colors
