# 4. Projects

A BLiPS Project is a text file describing a lighting project in either
[YAML](https://yaml.org) or [JSON](https://json.org) format.

**Example 1**: a simple Project file written in YAML

```
shape: 50
animation: $bpa.strip.Wave
```

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/4-example-1.gif)

**Example 2**: a slightly larger Project file, written in JSON

```
{
    "shape": [32, 32],

    "run": {
        "fps": 60
    },

    "animation": {
        "typename": "$bpa.matrix.MatrixRain",
        "colors": ["blue", "yellow", "coral"]
    }
}
```

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/4-example-2.gif)


**Example 3**: the same Project file, written in YAML

```
shape: [32, 32]

run:
    fps: 60

animation:
    typename: $bpa.matrix.MatrixRain
    colors: [blue, yellow, coral]
```

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/4-example-3.gif)

### A Project is made up of _Sections_, and Sections have _Fields_.

Project files have ten possible Sections, many of them optional.  The Project
files above contain three Sections - `shape`, `run`, and `animation`.

The Project Sections are `aliases`, `animation`, `controls`, `driver`,
`drivers`, `layout`, `numbers`, `path`, `run`, and `shape`... but you will
probably never use many of these.

Sections can have Fields - for example, the `run` Section above has the Field
`fps: 60`.

The most important Sections are `animation`, `shape`, and `driver`, which appear
in almost every Project:

* `animation` describes how your lights are animated
* `shape` shows how your lights are laid out in 1, 2, or 3 dimensions
* `driver` configures the hardware driver that controls the actual lights

### Class Sections and Value Sections

_Value Sections_ contain simple things like strings, numbers, lists, or
dictionaries.  The five Value Sections are `aliases`, `numbers`, `path`, `run`,
and `shape`.

Nearly all the excitement in BLiPS is in the Class Sections!

_Class Sections_ are Python objects.  There are five Class Sections:
`animation`, `controls`, `driver`, `drivers` and `layout`.

Each Class Section has a special Field `typename` containing the name of its
Python Class.

The Python Class determines what that Section does, and which Fields can be set
on it.  The `typename` field let you load not just BLiPS code, but your own code
or third-party code.

BLiPS comes with a large number of predefined Animations, Controls, Drivers and
Layouts, and you can put them together and customize them simply by writing a
Project, without any programming.

More, if you know a little Python you can extend them or modify a copy, or just
write your own from scratch.

### Fields

Each Section has named _Fields_ - values that you can set in that Section.

In Example 2 and 3 above, the `run` Section has the Field `fps` with value
`60` (fps meaning "frames per second"), and the `animation` Section has the
Field `imagePath` with value `/Users/tom/Documents/giphy-zoom.gif `.

A Value Section always has the same Fields - for example, the `run` Section
always has the `fps` Field in any Project.

On the other hand, a Class Section will have different Fields depending on its
`typename`.

For example, many Animations have no Fields at all and do exactly one thing,
like the Animation `.tests.PixelTester`:

**Example 4**:  An Animation that runs a simple test on a strip of 32 pixels

```
shape: 32
animation:
    typename: .tests.PixelTester
```

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/4-example-4.gif)


On the other hand, the `.sequence` Animation requires a Field `animations`,
a list of Animations that are played in sequence.  It also has an optional
Field `length` which sets the length of each subsequence.


**Example 5**:  This Animation runs four Animations, each for two seconds, in a
  loop, and displays the result on a 32x32 pixel display.

```
shape: [32, 32]

animation:
    typename: .sequence
    length: 2
    animations:
        - $bpa.matrix.ImageAnim
        - $bpa.matrix.ImageShow
        - $bpa.matrix.ImageDissolve
        - $bpa.matrix.ScreenGrab
```

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/4-example-5.gif)

# A summary of the Sections

## Class Sections

* `driver`: The output Driver for the hardware or simulator
* `drivers`: Used if there's more than one Driver.  If the `drivers` Section is
  non-empty, the `driver` Section becomes a template for `drivers`
* `layout`:  The Layout lays the lights out geometrically
* `animation`: The Animation animates the lights over time
* `controls`: Classes that use external input to control parts of
  the Project

## Value Sections

* `aliases`: Aliases are a shorthand to save typing
* `numbers`: Selects between plain old Python lists and faster, more powerful
numpy lists
* `path`: `path` is added to the `PYTHONPATH` to allow loading of custom
  libraries
* `run`: `run` controls how the topmost Animation is executed - how fast it
  runs, for how long or for how many times, and more
* `shape`: The shape of the layout - `length` for strips, `[width, height]` for
matrices and `[x, y, z]` for cubes

_Previous:_ [3. The `bp` program](3-The-bp-program.md)
. . . . . . . . . . . . . . . . . . . . . . . .
_Next:_  [5. The `animation` Section](5-The-animation-Section.md)

---


```
shape: [64, 4]
animation: $bpa.strip.LarsonScanners.LarsonScanner
```

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/4-footer.gif)
