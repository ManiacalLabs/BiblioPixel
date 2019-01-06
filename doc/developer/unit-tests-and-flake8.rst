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


Protip: assign this to a keystroke!
======================================

How to do this depends entirely on your editor or development system, but I have
it set up so a single keystroke runs both of these tests and gives me an error
if either one of them fails.

(I have the key F7 mapped to this command:  (save everything, then),
``flake8 && pytest test``.)

When I am developing, I run this after each tiny but complete change I make,
just by hitting a single key.  On a productive day, I will run this literally
a couple of hundred times.
