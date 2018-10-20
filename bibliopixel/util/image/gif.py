import io, os, pathlib
from .. import log
from . import file_writer


class Writer(file_writer.FileWriter):
    def _write(self, filename, frames, fps, loop=0, palette=256):
        """
        Write a series of frames as a single animated GIF.

        :param str filename: the name of the GIF file to write

        :param list frames: a list of filenames, each of which represents a single
            frame of the animation.  Each frame must have exactly the same
            dimensions, and the code has only been tested with .gif files.

        :param float fps:
            The number of frames per second.

        :param int loop:
            The number of iterations. Default 0 (meaning loop indefinitely).

        :param int palette:
            The number of colors to quantize the image to. Is rounded to
            the nearest power of two. Default 256.
        """

        from PIL import Image
        images = []
        for f in frames:
            data = open(f, 'rb').read()
            images.append(Image.open(io.BytesIO(data)))

        # GIF duration is only measured to a hundredth of a second
        duration = round(1 / fps, 2)
        im = images.pop(0)
        im.save(filename,
                save_all=True,
                append_images=images,
                duration=duration,
                loop=loop,
                palette=palette)
        # See also https://github.com/python-pillow/Pillow/issues/3255


from .. import deprecated
if deprecated.allowed():  # pragma: no cover
    from . old_gif import *  # noqa: F403
