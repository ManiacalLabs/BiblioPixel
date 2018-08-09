from . import wrapper
from .. util.image import gif_writer as _gif_writer


class GifWriter(wrapper.Wrapper):
    """
    An animation that writes animated GIFs for each frame in the contained
    animation."""

    def __init__(self, *args, filename='gif_writer', render=None,
                 divide=1, frames=128, time=0, scale=1.0, gif_options=None,
                 tmp_dir=None, **kwds):
        """
        :param str filename: Base filename to write the animated GIF file

        :param dict render: Parameters to the renderer function -
            see ``bibliopixel.util.image.render.renderer``

        :param int divide: If greater than 1, only rendered one in ``divide``
            frames

        :param int frames: Number of frames to write

        :param float time: Total time to write.  If non-zero, takes precedence
            over `frames`

        :param float speed: the length of the GIF is scaled by this factor, so
            if speed=2 then a 1 second animation will become a 2 second GIF.

        :param dict gif_options: Options to
            ``bibliopixel.util.image.gif.write_animation``

        :param str tmp_dir: If set, write individual GIF frame files to this
            directory, and do not delete them when done.  For testing purposes.
        """
        super().__init__(*args, **kwds)
        self._writer = _gif_writer.GifWriter(
            filename, render, divide, frames, time, scale, gif_options, tmp_dir)
        self._writer.set_layout(self.layout)

    def step(self, amt=1):
        super().step(amt)
        if self._writer.step(self.cur_step):
            self.completed = True

    def set_project(self, project):
        super().set_project(project)
        self._writer.set_project(project)

    def cleanup(self, clean_layout=True):
        super().cleanup(clean_layout)
        self._writer.write()
