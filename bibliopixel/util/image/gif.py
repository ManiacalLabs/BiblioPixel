import os, pathlib
from .. import log


# PIL has a limit on how many image files can be open at once - you get an
# exception when you try to open more files than that in save_images.  The exact
# number varies for some unknown reason but I consistently was able to get at
# least 240, but I use 192 for safety.
MAX_IMAGES_IN_MEMORY = 192
WINDOW_SIZE = MAX_IMAGES_IN_MEMORY // 2


def write_animation(filename, frames, **gif_options):
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

    if len(frames) > MAX_IMAGES_IN_MEMORY:
        log.warning('Number of frames %d exceeds MAX_IMAGES_IN_MEMORY %d',
                    len(frames), MAX_IMAGES_IN_MEMORY)

    from PIL import Image
    images = [Image.open(f) for f in frames]
    im = images.pop(0)
    im.save(filename, save_all=True, append_images=images, **gif_options)


def write_animation_windowed(filename, frames, window_size, **gif_options):
    first_time = True
    while frames:
        window = frames[:window_size]
        if first_time:
            first_time = False
        else:
            # Read the result of the previous step, and put it in at the start
            # of the list.
            window.insert(0, filename)

        # TODO: cut up durations list here
        write_animation(filename, window, **gif_options)
        frames = frames[window_size:]


"""
This is probably not used and should likely be replaced by the code
in BiblioPixelAnimations.matrix.ImageAnim
"""


from .. import deprecated
if deprecated.allowed():
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
