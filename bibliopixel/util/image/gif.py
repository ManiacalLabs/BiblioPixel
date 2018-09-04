import io, os, pathlib
from .. import log


def write_gif(filename, frames, **gif_options):
    """
    Write a series of frames as a single animated GIF.

    :param str filename: the name of the GIF file to write

    :param list frames: a list of filenames, each of which represents a single
        frame of the animation.  Each frame must have exactly the same
        dimensions, and the code has only been tested with .gif files.

    The whole gif_options dictionary is passed as keywords to PIL.Image.save.
    Its individual options are documented here as taken from the PIL
    documentation:

    :param int loop:
        The number of iterations. Default 0 (meaning loop indefinitely).

    :param float, list duration:
        The duration (in seconds) of each frame. Either specify one value
        that is used for all frames, or one value for each frame.
        Note that in the GIF format the duration/delay is expressed in
        hundredths of a second, which limits the precision of the duration.

    :param float fps:
        The number of frames per second. If duration is not given, the
        duration for each frame is set to 1/fps. Default 10.

    :param int palette:
        The number of colors to quantize the image to. Is rounded to
        the nearest power of two. Default 256.
    """

    from PIL import Image
    images = []
    for f in frames:
        data = open(f, 'rb').read()
        images.append(Image.open(io.BytesIO(data)))

    im = images.pop(0)

    if 'loop' not in gif_options:
        gif_options['loop'] = 0
        # See https://github.com/python-pillow/Pillow/issues/3255

    im.save(filename, save_all=True, append_images=images, **gif_options)


"""
This is probably not used and should likely be replaced by the code
in BiblioPixelAnimations.matrix.ImageAnim
"""


from .. import deprecated
if deprecated.allowed():  # pragma: no cover
    def convert_mode(image, mode='RGB'):
        """Return an image in the given mode."""
        deprecated.deprecated('util.gif.convert_model')

        return image if (image.mode == mode) else image.convert(mode=mode)

    def image_to_colorlist(image, container=list):
        """Given a PIL.Image, returns a ColorList of its pixels."""
        deprecated.deprecated('util.gif.image_to_colorlist')

        return container(convert_mode(image).getdata())

    def animated_gif_to_colorlists(image, container=list):
        """
        Given an animated GIF, return a list with a colorlist for each frame.
        """
        deprecated.deprecated('util.gif.animated_gif_to_colorlists')

        from PIL import ImageSequence

        it = ImageSequence.Iterator(image)
        return [image_to_colorlist(i, container) for i in it]


if __name__ == '__main__':
    pass
