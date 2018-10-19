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


from .. import deprecated
if deprecated.allowed():  # pragma: no cover
    from . old_gif import *  # noqa: F403
