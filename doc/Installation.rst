Installation
============

For an AllPixel specific quick start guide with examples, check out the
`AllPixel
Wiki <https://github.com/ManiacalLabs/AllPixel/wiki/Library-Install-and-Strip-Example>`__

Requirements
------------

BiblioPixel v3 requires Python 3.4 or higher. Python 2 is deprecated and
we urge you to move away from it - if your application requires Python
2, then there's an unsupported legacy `BiblioPixel
2 <https://github.com/ManiacalLabs/BiblioPixel2>`__ that works with
Python 2.7.

It is recommended (but not necessary) to use
```virtualenv`` <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`__
to isolate your installation of BiblioPixel. If you do not use
``virtualenv`` and are running on either Linux or MacOS, then in the
instructions below, you need to use ``sudo pip`` instead of ``pip``.

Installation
------------

The easiest way to acquire BiblioPixel is using
`pip <http://pip.readthedocs.org/en/latest/installing.html>`__. If you
don't already have pip the easiest way is to download and run
`get-pip.py <https://bootstrap.pypa.io/get-pip.py>`__. Then install
BiblioPixel as follows:

::

    pip install BiblioPixel

If you are not using a virtual environment your system default python is
likely v2.7. If so, you will need to install using
``pip3 install BiblioPixel`` or ``python3 -m pip install BiblioPixel``.

This will automatically install the entire package and make it available
to import from anywhere in python 3. Required dependencies will also be
installed automatically with the exception of a few optional packages
specific to sub-modules that you may never need. If you try to run part
of BiblioPixel that requires another dependency, it will print
instructions for obtaining that package to the console.

You may now either use the code directly or use the [[bibliopixel CLI]].
