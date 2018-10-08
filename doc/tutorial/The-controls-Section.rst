The ``controls`` Section
-------------------------------

The optional ``controls`` Class Section is an advanced feature which allows you
to change Fields or call methods on your Project while it is running in response
to external events in real-time.

Here's the high-level picture: a Control converts an incoming RawMessage to a
Message, and routes that Message to an Address with a list of Actions.

Currently BiblioPixel has the following Control Classes:

``artnet``
  Receive lighting data from a network

``keyboard``
  Keyboard events on a standard computer keyboard

``midi``
  Incoming MIDI events

``rest``
  Brings up a REST server which accepts information incoming

This page is going to talk about Controls in general, and the next page will
discuss routing, Addresses, and Actions in more detail.


Controls operate independently of everything else
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Controls are designed to be completely independent of the rest of BiblioPixel.

This means that one person can write a specific Control in Python, another one
can write an Animation in Python, and a third person can write a Project that
connects the Control to the Animation *without programming* - just by filling
the Control Section in a Project.

All Controls so far run in an independent Python thread, and there's no reason
they couldn't run in a different process (and this will be an option in later
releases of BiblioPixel).


How Controls work!
^^^^^^^^^^^^^^^^^^^^^^^

#. A Control receives or generates a Raw Message.

#. A Raw Message can be anything: MIDI, a keystroke, packets from the Internet,
   or some hardware data.

#. The Raw Message is converted into an ordered dictionary called the Message.

#. The Message is routed to an Address with the ``routing`` dictionary, or
   discarded if it can't be routed.  This will be explained in more detail a
   little later.

#. The Address has a list of Actions that it performs with the Message.  These
   typically set values in the Project, but can also be programmed to do any
   operation you need.


Monitoring controls
^^^^^^^^^^^^^^^^^^^^^^^^^^^

``bp`` has a simple utility to monitor Control Messages.  Right now it only works on
MIDI and keyboard inputs.

The examples in the Controls section use a simple MIDI fader control you can get
cheaply in any music store.  You should configure it so that its first four
faders are sending "MIDI control changes" on Control Numbers 0, 1 2, and 3.

Plug the MIDI fader control into your computer, and enter the command below:

.. code-block:: bash

    $ bp monitor midi

You should see output much like the following:

.. code-block:: bash

   control_change 0 87/127
   control_change 0 89/127
   control_change 2 14/127

If you don't see something like this, then you aren't receiving MIDI - either
check that MIDI is being received with some other program, and then ask us for
help.


Control Fields
^^^^^^^^^^^^^^

Each Class of Control has its own specific Fields, but all Controls share the
following optional fields:

``pre_routing``
    A list of Actions that get the entire Message before it gets routed.

``routing``
    A dictionary that routes Messages to Actions.

``errors``
    How to handle any software errors that occur - default is ``'raise'``
    If ``errors`` is ``'raise'``\ , then a Python exception is raised.
    If ``errors`` is ``ignore``\ , then software errors are silently ignored
    If ``errors`` is ``report``\ , then they are reported.

``verbose``
    Defaults to False.  If ``verbose`` is True, the Control will report
    everything that happens to it in detail.


Normalized numbers
^^^^^^^^^^^^^^^^^^

Controls have to handle many different sorts of numbers, and it's going to be
hard for the user to write Projects that work well if the numbers are all over
the place!

This is why the Controls sections *normalizes* many of the numbers that it
receives in the Raw Message before putting them into the Message.

For example, a raw MIDI Note On Message has a velocity that can be any number
from 0 to 127.  The Controls Section normalizes that to be a number from 0 to 1
by dividing it by 127 before storing it in the Message.

A different example: a raw MIDI Pitch Bend Message is a number from 0 to 16383,
where 8192 means "no bend".  In this case, the Control Section normalizes this
number into the range between *-1* and 1, because Pitch Bend is logically a
device that has positive (bend up) and negative (bend down) values.

The "expected range" for numbers is between 0 and 1 for values that can't be
negative (like keyboard velocity), and between -1 and 1 for values that can be
negative (like pitch bend), but BiblioPixel is tolerant of normalized values
that are out of the expected range

For example, it is perfectly possible to turn up the brightness in an Animation
to be greater than 100% (255), and you'll get perfectly reasonable results.  You
can even set brightness or other such numbers to be negative values and nothing
will go wrong - you'll just see black.

So don't be afraid to hook one value up to another in your ``control`` Section -
you can't break anything.


Extractors
^^^^^^^^^^

Nearly all Controls have an optional ``extractor`` Class Section.

An Extractor is an adaptor and a filter to translate "lots of real world data,
most of which you don't want" into "a small amount of specific data you do
want".

Technically, an Extractor turns a Raw Message into an ordered Message
dictionary with specific normalized Fields in a specific order, but you can
use an Extractor fairly intuitively.

A Control class has default values for its Extractor, or you can override these
values in your Project.

[API-DOC: link to the generated docs, which are pretty good for this
class] Most of the time, you'll only be wanting to change the ``accept``\ ,
``omit`` or ``reject`` Subfields in the ``extractor`` field of the Control.


----

.. code-block:: yaml

    shape: [64, 24]
    animation:
      typename: $bpa.matrix.Mainframe


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/12-footer.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/12-footer.gif
   :alt: Result
   :align: center
