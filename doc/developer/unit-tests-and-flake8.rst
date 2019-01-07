Unit tests and flake8
--------------------------

A majority of the code BiblioPixel code has _unit tests_ - tests that
are automatically run for every commit that test all the functionality is
working.  At this writing, there are 456 tests.

Also, we want to keep the code consistent with the standard Python style
which is explained neatly in
`this article <https://realpython.com/python-pep8/>`_ so there's a tool
called ``flake8`` that is run to find these style violations!

Both of these code quality tools are run automatically using `Travis CI
<https://travis-ci.org/>`_ for each pull request, but you will want to do
these tests on your own machine before submitting a pull request!

The programs to do this were already installed in a previous step, so here's
what you need to do!  Go to the root BiblioPixel directory and type:

.. code-block:: bash

    $ flake8
    $ pytest test

The first statement tests the code for style errors;  the second one runs all
the unit tests.

You don't have to wait until you have code to try it - do it now!  If everything
is OK, then all the tests should work.


Fixing bugs
==================

We welcome any and all bug fixes, but the best way to fix a bug is like this:

1. Create a test which demonstrates the problem - in other words, a test which
   fails because of the bug.

2. Fix the bug.

3. Demonstrate that the test now works.

The huge advantage of this is that it makes it harder for bugs to reappear -
"regressions", a problem which is very common in larger projects.


Writing new code
=====================

While we recognize that it is not always possible to write automatic tests for
all code, systematic automatic testing results in much more reliable code.

If you are adding new functionality to BiblioPixel, we would love it if you
added new tests for that functionality.

Good tests are hostile ;-) and try really hard to break the code with
unreasonable or extreme cases - what we call "edge cases".

It's OK for code to fail on actuall wrong inputs of course, but even then, it's
better if it fails in a clear and understandable way.  If you look at the
existing tests, there are dozens of tests that show that we handle errors
correctly and clearly.

Protip: assign these tests to a keystroke!
======================================================

How to do this depends entirely on your editor or development system, but I have
it set up so a single keystroke runs both of these tests and gives me an error
if either one of them fails.

In specific, I have the F7 key mapped to a command that saves everything, then
runs ``flake8 && pytest test``.

When I am developing, I run this after each tiny but complete change I make,
just by hitting a single key.  On a productive day, I will run this
a couple of hundred times, quite literally.
