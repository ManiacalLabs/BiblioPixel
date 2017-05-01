The `bibliopixel` command line program.
==================

The program `bibliopixel` is the command line front end to BiblioPixel, the LED
control system.

You can use `bibliopixel` to run demos or your own projects, to set and get
defaults for projects, or to discover hardware devices attached to your
computer.


Basic usage of `bibliopixel`.
----

The program is installed automatically when the BiblioPixel system is installed
and can be executed from the command line by typing `bibliopixel <command>`
and hitting return.

The possible commands at this writing are `all_pixel`, `devices`, `demo`,
`help`, and `run` and they fit into four categories:

* Hardware: `all_pixel` and `devices` discover and list devices.

* Demo: `demo` runs premade demos in your browser.

* Help: `help` gives detailed instructions for each command.

* Project: `run` runs BiblioPixel projects.


Hardware commands
----

BiblioPixel's hardware commands allow you to discover and list Maniacal Lab's
AllPixel hardware interfaces, or generic serial port interfaces.

`bibliopixel all_pixel`

TBD

---

`bibliopixel devices`

TBD

---

Demo command
----

The BiblioPixel system comes with many demos.  All of these use the SimPixel
WebGL driver, which means that you can execute them on any computer, even if
you don't have any lighting hardware.


`bibliopixel demo`

Lists all the demos and runs a random one.

---

`bibliopixel demo list`

Lists all the demos.

---

`bibliopixel demo <demo name>`

Runs one of the BiblioPixel demos by name.

Example: `bibliopixel demo bloom`

---

Help command
----

The `bibliopixel` program comes with online help.

`bibliopixel help`

Prints general help for the `bibliopixel` program.

---

`bibliopixel help <command>`

Prints more specific help for one command.

Example: `bibliopixel help demo`

---


Project command
----

For more information about projects, see [here](Projects.md).

At this time there is only one Project command: `run`.


`bibliopixel run <project file>`

Runs a project found in a file.  You can use

* Paths relative to your current directory (e.g. `bibliopixel run flashy.json`)
* Absolute paths (e.g. `bibliopixel run /home/stuff/black.json`)
* User-relative paths (e.g. `bibliopixel run ~/my-lites.json`)
