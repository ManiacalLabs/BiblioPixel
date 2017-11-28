A BiblioPixel path identifies a Python library used in a BiblioPixel
project, and comes in one of two types:

-  A *file path* is a path to a file directory that contains the
   library. This works just like
   ```PYTHONPATH`` <https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH>`__.

-  A *gitty path* is the address of a library that is located on a
   public Git repository. This feature uses the
   `gitty <https://github.com/timedata-org/gitty>`__ library to
   dynamically load Python libraries from public repositories.

Examples of gitty paths
-----------------------

::

    //git/github.com/ManiacalLabs/BiblioPixelAnimations
    //git/github.com/ManiacalLabs/BiblioPixelAnimations/dev
    //git/github.com/ManiacalLabs/BiblioPixelAnimations/dev/f7b3660  

In general, a gitty path looks like:

::

    //git/<provider>/<user>/<project>[/<branch>[/<commit-id>]]

where the ``branch`` and ``commit-id`` components are optional.

SECURITY WARNING ABOUT GITTY PATHS
==================================

When you use a gitty path, you are running Python code from some public
Git repository on your machine. If the person or organization who owns
that Git repo is malicious, they could run any code they pleased on your
computer. Only use gitty paths to refer to sources *that you completely
and 100% trust.*
