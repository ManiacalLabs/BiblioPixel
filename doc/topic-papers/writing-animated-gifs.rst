Writing Animated GIFs from Projects
-----------------------------------------------

Basic Usage
==================

The ``-g``/``--gif`` flag to ``bp`` renders a Project as an animated GIF by
temporarily replacing the driver in the project with a ``GifWriter`` driver.

Examples:
~~~~~~~~~~~~

.. code-block: bash

    bp my_project.yml --gif=output-file.gif
    bp my_project.yml --gif  # Renders to my_project.gif


Advanced Usage
===============

You can put a ``GifWriter`` driver in your code for more control over the
output.

.. code-block: yaml

   driver:
     typename: gif_writer
     filename: lovely-gif.gif
     speed: 2

     render:
       color: 'dark grey'
       ellipse: false
       pixel_width: 5
       frame: 0
       padding: 2

This would render the project to a file called lovely-gif.gif, twice real-time
speed, square pixels of width 5, padded with 2 pixels of dark grey background.

You can see all the ``GifWriter`` options `here <https://github.com/ManiacalLabs/BiblioPixel/blob/master/bibliopixel/util/image/gif_writer. py#L4-L16>`_
and `here <https://github.com/ManiacalLabs/BiblioPixel/blob/master/bibliopixel/drivers/gif_writer. py#L10-L36>`_\ .
