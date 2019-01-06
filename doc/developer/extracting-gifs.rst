Automatically extracting GIFs from the documentation
----------------------------------------------------------

GIF extraction; and, why the preprocessing phase?
===================================================

The documentation has a really neat if somewhat overengineered feature where
you can embed a BiblioPixel project in a documentation page, and it's
automatically turned into an animated GIF that shows what that project would
look like if run!

For example, if you look at the ``bp-code-block::` section in `this document
 <https://github.com/ManiacalLabs/BiblioPixel/blob/master/doc/README.rst>`_,
it corresponds to the Project and image at the bottom of
`this page <https://maniacallabs.github.io/BiblioPixel/>`_.

Unfortunately, this adds complexity to the build, and requires this
preprocessing phase, and that leads to some `some annoyances
<https://github.com/ManiacalLabs/BiblioPixel/issues/1117>`_
but we decided that it was worth it because animated GIFs are cool.

Most of the time you as a developer won't need to do this.

We try to make sure that each new page has a unique animation on it,
just because we can, so if you write a new page, you could also add your own
(although we'd take any documentation you wrote, even if it didn't have one) -
and then you'd want to run the GIF extraction.

Also, if you change any of the examples (in ``.. bp-code-block::`` sections)
in the documentation then you'd definitely want to run the GIF extraction.

Because these GIF files are quite large, they live in a separate repository -
https://github.com/ManiacalLabs/DocsFiles

Start by forking that repository in github.com.

Then check it out: from the directory _above_ the
BiblioPixel/BiblioPixelAnimation directories, type:

.. code-block:: bash

    # If you have an SSH certificate:
    $ git clone git@github.com:<your-git-user>/DocsFiles.git

    # otherwise:
    $ git clone https://github.com/<your-git-user>/DocsFiles.git

    # Go back to where you came from:
    $ cd BiblioPixel

Now you're ready to perform the GIF extraction.  Type:

.. code-block:: bash

    $ scripts/documentation/extract-gif

This extracts GIFs from all the changed projects in the documentation.

Now, this step does not actually push the changes to git - instead it puts
them into that parallel ``DocsFiles`` directory.

When you are finished with your changes, you can run the script:

.. code-block:: bash

    $ scripts/documentation/deploy

which will push the changes in that ``DocsFiles`` project to your
fork of it, and you can prepare a pull request to get them committed
so that everyone can see it.

Also, please note that there is unfortunately no convenient way to view the
changed GIFs inside the HTML code, so you have to open the changed GIFs by
hand to see the results.  This isn't likely to change because it seems
extremely hard to get working.
