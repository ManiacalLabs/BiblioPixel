# 12. The `controls` Section

The `controls` Class Section  is an advanced feature which allows you to change
values in your Project in real-time,  while it is running.

`controls` are completely optional in a Project.

They are designed so that one person can write a specific Control in Python,
another one can write an Animation in Python, and a third person can write a
Project that connects the Control to the Animation _without programming_ - just
by filling out the fields in a Project.

Currently BLiPS has the following Control Classes:

* `artnet`: receive lighting data from a network
* `keyboard`: keyboard events on a standard computer keyboard
* `midi`: incoming MIDI events
* `REST`: brings up a REST server which accepts information incoming

There are also tools to make it possible to write your own Control Class.

### Life of a Message

A Control routes an incoming Message to an Address.

1. A Control receives or generates a Raw Message.

2. A Raw Message can be anything: MIDI, a keystroke, packets from the Internet,
   or some hardware data.

3. The Raw Message is converted into an ordered dictionary called the Message.

4. The Message is routed to an Address with the `routing` dictionary, or
   discarded if it can't be routed.  This will be explained in more detail a
   little later.

5. The Address has a list of Actions that it performs with the Message.  These
   typically set values in the Project, but can also be programmed to do any
   operation you need.

### Normalized numbers

Controls have to handle many different sorts of numbers, and it's going to be
hard for the user to write Projects that work well if the numbers are all over
the place!

This is why the Controls sections _normalizes_ many of the numbers.
Normalizing means rougly "keep the numbers' magnitude <= 1".

For example, a MIDI Note On Message has a velocity that can be any number from 0
to 127.  The Controls Section normalizes that to be a number from 0 to 1.

A different example: a MIDI Pitch Bend Message is a number from 0 to 16383,
where 8192 means "no bend".  In this case, the Control Section normalizes this
number into the range between _-1_ and 1, because Pitch Bend is logically a
device that has positive (bend up) and negative (bend down) values.

BLiPS is tolerant of normalized values that are out of range.

For example, it is perfectly possible to turn up the brightness in an Animation
to be greater than 100% (255), and you'll get perfectly reasonable results.  You
can even set brightness or other such numbers to be negative values and nothing
will go wrong - you'll just see black.

So don't be afraid to hook one value up to another in your `control` Section -
you can't break anything.

### Extractors

The basic definition of a Control is deliberately very general, in order to allow
anyone to write any sort of control they please. In practice, most developers
want more structure, and so most Controls are ExtractedControls - Controls that
use an Extractor.

An Extractor turns a Raw Message into a Message dictionary with specific Fields
in a specific order, containing normalized values.

The Control sets values for its Extractor, but they can be overwritten in the
Project.
[TBD: link to the generated docs, which are pretty good for this class]
Most of the time, you'll only be wanting to change `accept`, `omit` or `reject`.


### Routing

The Control handles everything automatically, except for the routing, where you
need to tell it what to do by filling out a `routing` dictionary in the Project.

Here's a series of examples involving a simple MIDI fader control.  You should
configure it so that its first four faders sending MIDI control changes on
Control Number 0, 1 2, and 3.

First, plug the fader control in, make sure it's configured and then enter `bp
monitor midi` at the command line.  You should see a series of events like this:

```
control_change 2 87/127
control_change 2 89/127
control_change 2 90/127
```

If you don't see something like this, then you aren't receiving MIDI - either
check that MIDI is being received with some other program, and then ask us for
help.

Now run [this project](midi-1.yml):

**Example 1**: A MIDI control project
```
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
```

### Control Fields

Each Class of Control has its own Fields, but all Controls share the following
fields:

* `pre_routing`: A list of Actions that get the Message before it gets routed.

* `routing`: The dictionary that directs Messages to Actions.

* `errors`: How to handle any software errors that occur - default is `'raise'`
   If `errors` is `'raise'`, then a Python exception is raised.
   If `errors` is `ignore`, then software errors are silently ignored
   If `errors` is `report`, then they are reported.

* `verbose`: defaults to False.  If set to True, the Control will report
  everything that happens to it in verbose details.


_Previous:_ [11. The Serial Driver](11-The-serial-Driver.md)
. . . . . . . . . . . . . . . . . . . . . . . .
_Next:_ ?

---


```
shape: [64, 24]
animation:
  typename: $bpa.matrix.Mainframe
```

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/12-footer.gif)
