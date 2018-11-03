Types of Typenames
-----------------------------

This Section is fairly advanced and can be skipped on first reading.

You can write Typenames in four formats:

1. Absolute Typenames
================================

An Absolute Typename is a full Python pathname of a class or function like
``math.log`` or ``bibliopixel.animation.tests.PixelTester``.

Absolute Typenames start with a letter and can contain only letters, numbers,
the period ``.``\ , and the underscore ``_``.

So ``x23.he_is_13.yes`` is an Absolute Typename but neither ``23x.h`` nor
``this-has-dashes`` nor ``this has spaces.no`` nor ``oops!`` are Absolute
Typenames.

2. Relative Typenames
================================

To save typing, you can specify typenames relative to the base module for
that Class Section.  For example, the Absolute Typename
``bibliopixel.animation.tests.PixelTester`` can be shortened to
the Relative Typename ``.tests.PixelTester``

Relative Typenames start with a ``.`` and then follow the same rules as Absolute
Typenames.

3. File Typenames
================================

You can directly load Python code from a file on your drive this way:
``/home/pi/Documents/myAnimation.py``

File Typenames always start with ``/``.

4. Git Repo Typenames
==============================================

You can directly load code from a Github repo.

``https://github.com/ManiacalLabs/BiblioPixelAnimations/blob/master/BiblioPixelAnimations/matrix/MatrixRain.py``


WARNING WARNING WARNING!
-------------------------------

Git Repo Typenames allow you to load arbitrary code from the internet and
execute it.

Malicious code that you downloaded this way could do anything, including erasing
all your data or stealing money from your accounts.  ONLY use Git Repo Typenames
if you *completely and 100%* trust the repo that you are loading from.
Remember, there's nothing preventing people from changing code that's perfectly
safe today to be malicious tomorrow.

The first time that you use a new Git Repo, ``bp`` will prompt you from the
command line to whitelist that site.  *Think long and hard* before you do this!
Or simply choose not to use this feature, and download the code yourself as you
need it.

.. bp-code-block:: footer

   shape: [96, 16]
   animation:
     typename: $bpa.strip.Wave.WaveMove
     color: 'royal blue'
