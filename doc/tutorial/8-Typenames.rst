8. Typenames, and the ``path`` and ``aliases`` Sections
============================================================

8.1. What is a Typename?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

BiblioPixel lets you load projects, parts of projects, or even Python code from
your local drive or from the Internet, and Typenames are BiblioPixel's way of
identifying what code that is.

A *Typename* names a Python class.  Typenames appear in Class Sections only -
i.e. ``animation``\ , ``controls``\ , ``drivers``\
, or ``layout``\.

For easier reading and writing of Projects, if a Class Section is a string
instead of a dictionary, that string used as the ``typename`` - so these two
projects mean the same:

.. code-block:: yaml

       animation:
         typename: .sequence


.. code-block:: yaml

       animation: .sequence


You can write Typenames in four formats.

8.2. Absolute Typenames
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An Absolute Typename is a full Python pathname of a class or function like
``math.log`` or ``bibliopixel.animation.tests.PixelTester``.

Absolute Typenames start with a letter and can contain only letters, numbers,
the period ``.``\ , and the underscore ``_``.

So ``x23.he_is_13.yes`` is an Absolute Typename but neither ``23x.h`` nor
``this-has-dashes`` nor ``this has spaces.no`` nor ``oops!`` are Absolute
Typenames.

8.3. Relative Typenames
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To save typing, you can specify typenames relative to the base module for
that Class Section.  For example, the Absolute Typename
``bibliopixel.animation.tests.PixelTester`` can be shortened to
the Relative Typename ``.tests.PixelTester``

Relative Typenames start with a ``.`` and then follow the same rules as Absolute
Typenames.

8.4. File Typenames
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can directly load Python code from a file on your drive this way:
``/home/pi/Documents/myAnimation.py``

File Typenames always start with ``/``.

8.5. Git Repo Typenames
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can directly load code from a Github repo.

``https://github.com/ManiacalLabs/BiblioPixelAnimations/blob/master/BiblioPixelAnimations/matrix/MatrixRain.py``


8.6 WARNING WARNING WARNING!
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

8.7. Type guessing
^^^^^^^^^^^^^^^^^^^^^^^^

BiblioPixel can often guess the name of the class you mean from the file or
module that it's in.  This saves a lot of repetition.

This happens in two cases:


+ If there is only one class in the file or module
+ or if there is exactly one class in the file or module whose name is
  "canonically the same" as the file or module name

Two names are "canonically the same" if they are the same when you throw away
all punctuation and make them lower case - so ``HelloWorld``\ , ``HELLO_WORLD``
and ``hello_world`` are canonically the same.


EXAMPLES: How to use Typenames in a Project.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Example 1**\ :  Simple animation, Absolute Typename

.. code-block:: yaml

       animation:
         typename: bibliopixel.animation.sequence.Sequence

For convenience, if the whole class section is a string, it's the ``typename``\ :

**Example 3**\ :  Same animation as in Example 1

.. code-block:: yaml

       animation: bibliopixel.animation.sequence.Sequence

**Example 4**\ :  Relative Typename

.. code-block:: yaml

       animation: .sequence.Sequence

**Example 5**\ :  Relative Typename with type guessing

.. code-block:: yaml

       animation: .sequence


----

.. code-block:: yaml

   shape: [96, 8]
   animation:
     typename: $bpa.strip.Wave
     color: coral


.. image:: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/8-footer.gif
   :target: https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/BiblioPixel/doc/tutorial/8-footer.gif
   :alt: Result
