# What is this `release_test`?

`release_test` is a battery of acceptance tests for BiblioPixel release testing.


# Tests.

A test is a Python program that tests some software or hardware feature.

Here's a list of all the tests, in the order that they are called by default.

* `unit`: run the Python unit tests
* `simpixel`: test strip, matrix, cube and circle animations in the browser
* `keyboard`: test the keyboard control
* `rest`: test the REST control
* `midi`: test the MIDI control
* `remote`: test the Remote animation
* `all_pixel`: test many LED types connected to an AllPixel

# Features

Not every system will have every piece of hardware but developers might still
want to run a subset of the tests.  A Feature represents some optional hardware
or software that may not be there on a test machine.

Tests optionally have Features associated with them, which means they are only
run if that Feature is present.

The features are

* `all_pixel`: is there an AllPixel attached?
* `browser`: is there a display with a browser attached?
* `keyboard`: are we doing keyboard tests?
* `midi`: can we receive MIDI?


# How to run the program.

1. Everything

```
    # Guess which features your platform supports, and runs all the tests.
    release_test
```


2. Run specific tests

```
    # Only run the tests `unit`, `midi`, and `rest`.
    release_test unit midi rest
```


3. Run with specific features

```
    # Set the features to be `browser` and `keyboard`.
    release_test --features=browser:keyboard
```


4. Run with both

```
    # Set the features to be just `browser` and run only the `simpixel` test.
    release_test simpixel --features=browser
```
