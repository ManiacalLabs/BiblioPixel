# BiblioPixel Basics

## What is BiblioPixel

In the BiblioPixel Light Programming System, Python command line program named
`bp` runs a JSON document called a **Project** which contains information about
your lighting hardware, how your lights are laid out, and how you want to
animate them - as well as a really nice lighting simulator.

Let's go through what all of this means.

## JSON

JSON is a simple and very popular way to represent structured data in
human-readable and editable text.

[Here's](https://www.digitalocean.com/community/tutorials/an-introduction-to-json)
a nice little introduction to JSON, and [here's](https://json.org) the full
specification of the format, which isn't very long at all.

## The lighting simulator: SimPixel

BiblioPixel has a sibling project, SimPixel, which lets you preview your
lighting animations in any modern browser.  This is extremely convenient as it
allows you develop and test animations in your browser and then deploy them to
your hardware installation when you know they are ready.

## The command line

BiblioPixel does not have a graphical user interface - it is a command line
program where you type commands at the command line in a terminal.

On Linux or MacOS, you need to run a program called Terminal comes with the
computer.  On Windows, it's [TBD].

In the documentation, terminal commands will be shown like this:

``````
$ bp color
red: (255, 0, 0)
``````

Everything after a ``$`` means something you type in.   In the above example,
you typed `bp color` and the program responded `red: (255, 0, 0)`.


## The `bp` program

The `bp` program's full name is "the BiblioPixel Project runner".  It is
automatically installed when you install `BiblioPixel`.  `bp` has all sorts
of **commands**, with names like `run`, `demo`, `info` and much more.

Try the `bp demo` command now!  Type:

``````
$ bp demo
``````

This runs the `demo` command, which runs a demonstration BiblioPixel animation
and pops up a web page with a visualization of that animation.

## Two ways to interrupt `bp` - control-C and `bp shutdown`

But this seems to run forever!

While animations can have a specific, fixed length like ten seconds, a lot of
them go on indefinitely.  How can you interrupt `bp` in the middle of running an
animation?

One answer is "control-C".  This keystroke interrupts almost any command line
program, not just `BiblioPixel`.

To send a control-C, hold down the Control key on your keyboard (often marked
CTR or CTR) and press the C key  a few times until the program stops running.

Sometimes you don't have a terminal with the `bp` program running the
application.  In that case, you can use the command `bp shutdown`.  Open a new
terminalin and type `bp shutdown` and it will  shut down the currently running
`bp` application wherever it is on your machine.

## `bp run` - the most important `bp` command.

By far the most important command is `bp run`.  This runs Projects, which is the
way to make your lights light up!

[TODO: they won't have a main BiblioPixel directory!]
Try it now - go to the main BiblioPixel directory and type
`bp run -s projects/01-matrix.json`

It's  important that you can just leave it out - you'll get the same result
with `bp -s projects/01-matrix.json`
