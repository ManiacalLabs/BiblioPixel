
What is this ``release_test``\ ?
==================================

``release_test`` is a battery of acceptance tests for BiblioPixel release testing.

Tests.
======

A test is a Python program that tests some software or hardware feature.

Here's a list of all the tests, in the order that they are called by default.


* ``unit``\ : run the Python unit tests
* ``simpixel``\ : test strip, matrix, cube and circle animations in the browser
* ``keyboard``\ : test the keyboard control
* ``rest``\ : test the REST control
* ``midi``\ : test the MIDI control
* ``remote``\ : test the Remote animation
* ``all_pixel``\ : test many LED types connected to an AllPixel

Features
========

Not every system will have every piece of hardware but developers might still
want to run a subset of the tests.  A Feature represents some optional hardware
or software that may not be there on a test machine.

Tests optionally have Features associated with them, which means they are only
run if that Feature is present.

The features are


* ``all_pixel``\ : is there an AllPixel attached?
* ``browser``\ : is there a display with a browser attached?
* ``keyboard``\ : are we doing keyboard tests?
* ``midi``\ : can we receive MIDI?


How to run the release tests in a clean environment
===============================

1. Create a new Python virtualenv

2. ``cd`` to the BiblioPixel root directory

3. ``source scripts/release_test/run.sh`` runs the release tests in ``/tmp`` -
   or use ``source scripts/release_test/run.sh <your-directory>``.

4. Delete the Python virtualenv so you don't accidentally use it again


How to run the program.
=========================

This depends on what you want to run:

#. Everything

.. code-block::

       # Guess which features your platform supports, and runs all the tests.
       release_test


#. Run specific tests

.. code-block::

       # Only run the tests `unit`, `midi`, and `rest`.
       release_test unit midi rest


#. Run with specific features

.. code-block::

       # Set the features to be `browser` and `keyboard`.
       release_test --features=browser:keyboard


#. Run with both

.. code-block::

       # Set the features to be just `browser` and run only the `simpixel` test.
       release_test simpixel --features=browser


 Note for MacOS users
 ===========================

 In order to test the keyboard control, you need to be running as root,
 with either:

     sudo
