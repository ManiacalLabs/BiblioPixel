Module *image*
==============

The image module provides tools for displaying images on a matrix and
therefore is only useful with [[Matrix]] instances. This module requires
that `Pillow <https://pillow.readthedocs.org/en/latest/>`__ (a fork of
PIL; Python Imaging Library) be installed. If not already installed, the
easiest way to obtain Pillow is through pip:

::

    pip install pillow

show\_image
~~~~~~~~~~~

(led, image\_path = "", image\_obj = None, offset = (0,0), bgcolor =
colors.Off, brightness = 255)

-  **led** - An [[Matrix]] instance
-  **image\_path** - A full or relative path to the image to load (PNG,
   JPEG, or BMP).
-  **image\_obj** - A pre-loaded Pillow
   `Image <https://pillow.readthedocs.org/en/latest/reference/Image.html>`__
   instance.
-  **offset** - Placement offset of the top-left corner of the image, in
   (x,y) coordinate tuple.
-  **bgcolor** - Background color to use for pixels with transparency.
   Useful if image must be blended against non-black background or if
   image contains black (off) pixels.
-  **brightness** - Amount to scale image brightness by (0-255)

show\_image() will load a static image and display it on the matrix. To
decrease load time, the imageObj parameter can be use to pre-load the
image into memory before displaying it. All pixels beyond the bounds of
the matrix will simply be discarded. No class is needed and it can be
called directly, as follows:

.. code:: python

    import bibliopixel.image as image
    image.showImage(led, "test.png", bgcolor = (64, 64, 64))
    #displays test.png with background of 25% white

loadImage
~~~~~~~~~

(led, imagePath = "", imageObj = None, offset = (0,0), bgcolor =
colors.Off, brightness = 255)

loadImage is nearly identical to `showImage <#showimage>`__ - all input
parameters are identical - except that it returns an image buffer as a
2D list of color tuples instead of writing it directly to the display.
An [[Matrix]] instance is still passed in so that it can gather details
about the display size and process the image accordingly. Mainly
intended for use with [[setTexture()\|Matrix#settexture]].

Class *ImageAnim*
-----------------

**ImageAnim has been moved to the
`BiblioPixelAnimations <https://github.com/ManiacalLabs/BiblioPixelAnimations>`__
repo**
