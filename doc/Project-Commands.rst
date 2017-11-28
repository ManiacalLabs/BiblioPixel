For more information about projects, see `here <Projects.md>`__.

There are two Project commands: ``run`` and ``clear_cache``.

--------------

``bibliopixel run <project file>``

Runs a project found in a file. You can use

-  Files in to your current directory (e.g.
   ``bibliopixel run flashy.json``)
-  Files relative to your current directory (e.g.
   ``bibliopixel run ../tricks/magic.json``)
-  Absolute paths (e.g. ``bibliopixel run /home/stuff/black.json``)
-  User-relative paths (e.g. ``bibliopixel run ~/my-lites.json``)
-  Web paths (e.g.
   ``bibliopixel run https://github.com/ManiacalLabs/BiblioPixel/blob/dev/test/project.json``)

--------------

``bibliopixel clear_cache``

Clears the gitty cache of Python projects downloaded from public git
repositories. See [[BiblioPixel Paths]] for more information on gitty.
