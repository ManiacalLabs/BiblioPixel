# 0. Before you start

You don't need to know how to program in order to use BLiPS but you do need to
be familiar with a few things.

### 1. The command line

BLiPS works from the command line - by typing commands into a terminal window
and seeing text responses.

You don't by any means have to be an expert on the terminal to use it BLiPS!

All you need is to be comfortable with entering commands and pressing return,
and with the idea of directories and the current directory.


### 2. A text editor.

BLiPS uses text files to represent lighting projects, and so you will need some
sort of text editor.

You don't need anything too sophisticated.  Every computer comes with some sort
of simple text editor:

* `Notepad` on Windows
* `Text` on the Macintosh
* `vi` or `emacs` on Linux and the like

A popular text editor, SublimeText, works on all these platforms.

Please note that Microsoft Word does not work for this task of text editing -
it's a word processor, which is different, and it embeds all sorts of other
information in its documents, information that BLiPS cannot read.


### 3. YAML or JSON

YAML and JSON are two simple and popular ways to represent data as text.  BLiPS
accepts both.  All our examples are in YAML, because it's less typing - however,
many people who write Javascript prefer JSON and that works perfectly well.

BLiPS doesn't care about which file names you use, but it's neater to put JSON
data in files ending in .json and YAML data in files ending in .yml.

You can learn YAML by example, from reading this document.  If you're interested
in a bit more information, here's
[a link](https://github.com/darvid/trine/wiki/YAML-Primer).


**Example 1**: Some data in JSON:

```
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
    "shape": [32, 32]
}
```

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/0-example-1.gif)


**Example 2**:  The same data in YAML:

```
# This is a comment.

animation:
  typename: sequence
  length: 3

  animations:
    - .tests.PixelTester
    - {typename: fill, color: red}
    - $bpa.matrix.MatrixRain

shape: [32, 32]
```

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/0-example-2.gif)

YAML isn't just shorter and cleaner, it lets you write comments to yourself or
anyone else reading - by starting a line with the `#` character.

We're going to make heavy use of this "comment" feature in this documentation,
and we suggest you do too when writing your own lighting projects, unless your
memory is better than ours.


### 4. The animated GIFs in the documentation are on a short loop

Those pretty pictures are automatically generated from the example BLiPS
projects embedded in the documentation, so they fairly faithfully represent the
results you would get.

The one big difference is that that the GIFs loop (to keep their size down),
where the real animation would keep playing forever...


_Previous:_ [Documentation roadmap](../roadmap.md)
. . . . . . . . . . . . . . . . . . . . . . . .
_Next:_ [1. How To Install BLiPS](1-Installing-BLiPS.md)

```
shape: [64, 16]
animation: $bpa.matrix.Twinkle
```

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/0-footer.gif)
