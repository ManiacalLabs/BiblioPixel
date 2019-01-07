Using ``git``
----------------------------

BiblioPixel uses git for version control, so you need to know at least
a little about git.

Here's the high-level picture of how to develop BiblioPixel using git.

BiblioPixel is made up of two repositories.  The repo with the core that
handles devices and layouts and projects and runs animations is BiblioPixel;
many more Animations are collected into the BiblioPixelAnimation repository.

0. Creating a Github account
===================================

Start off by getting a user account on github if you don't have one.  In  this
page, we're going to call that account ``<your-git-user>``.

Once you have the account - it's a real drag if you have to type your password
in every time you do any git operation!  There are two ways around this:
`caching your password <https://help.github.com/articles/caching-your-github-password-in-git/]>`_,
or `using an SSH key <https://help.github.com/articles/connecting-to-github-with-ssh/>`_.
We strongly recommend you use one or the other of those methods.


1. Forking
======================

One time only, you need to _fork_ the two original repositories.  Forking means
to make a copy of a repository under your own name.  In this case, the fork will
also be on github.

Developers need a fork so that they can experiment with changes in a
repository that they do own, and then finally request those to be pulled to the
master fork that they do not own.

Go to https://github.com/ManiacalLabs/BiblioPixel and click the button in the
top right corner marked "Fork".  This will create a new repo named
``https://github.com/<your-git-user>/BiblioPixel``.

Then do the same with
https://github.com/ManiacalLabs/BiblioPixelAnimations to create a new repo named
``https://github.com/<your-git-user>/BiblioPixelAnimations``


2. Cloning
==============

On each machine you develop on, you need to _clone_ your two forks of the two
original repositories!

Cloning means downloading a snapshot of the code in your repositories onto the
machine you work on.  When you develop, you'll edit files in the clone on your
local machine and then push those changes to your forked repository.

First, create a clean directory where you are going to do all your work and
``cd`` to it.

We have written a script to do most of the work and it's
`here <https://raw.githubusercontent.com/rec/BiblioPixel/dev/scripts/developer/checkout.sh>`_.

Download the script, save it as ``checkout.sh``, and then type

.. code-block:: bash

    # IF you are using plain old https checkout:
    source checkout.sh <your-git-user> https

    # OR if you are using an SSH key (recommended):
    source checkout.sh <your-git-user> ssh

    #
    # Lots of stuff should happen there
    # If it looks OK, remove the installation script
    #
    rm checkout.sh

This checks out the two repositories and also adds two "git remotes"
to each of them:

* ``upstream`` is the master repo https://github.com/ManiacalLabs/BiblioPixel or
  https://github.com/ManiacalLabs/BiblioPixelAnimations

* ``rec`` is https://github.com/rec 's fork, the other principle developer.
  Having this remote is useful when troubleshooting issues with @rec.

3. Working in a new branch
=============================

Every change you want to make needs to be made in a new git _branch_ in your
fork, and it needs to be a copy

Here's how to make a new branch called ``new-branch``:

.. code-block:: bash

    # Fetch the most recent branches in the main repository
    git fetch upstream

    # Checkout a new, local branch called new-branch from upstream/dev
    git checkout -b new-branch upstream/dev

    # Push this branch to your fork
    git push --set-upstream origin new-branch

4. Creating commits and other such things
===========================================

This is beyond the scope of this document.  There are resources at e.g.
https://www.google.com/search?q=git+primer but none of them are great.  Please
report back if you find something really clear or useful.

5. Making pull requests
============================

The final stage in this process is to make a pull request - in other words,
ask the maintainers of BiblioPixel to review your code so that it can be
committed into the main program.

You do this from the github site.  You need to open the page for your new
branch, which will be a URL like
``https://github.com/<your-git-user>/BiblioPixel/tree/<your-branch-name>``

There will be a button near the right middle marked "Pull request".  Click on
that and go through the instructions.
