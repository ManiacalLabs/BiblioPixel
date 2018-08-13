from . driver_base import DriverBase
from .. util.image import gif_writer as _gif_writer


class GifWriter(DriverBase):
    """
    An animation that writes animated GIFs for each frame in the contained
    animation."""

    def __init__(self, *args, filename='gif_writer', render=None,
                 divide=1, frames=0, time=10, scale=1.0, gif_options=None,
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
        # TODO: this is duplicated here so that it's duplicated in the
        # documentation.  Is there a better way to do this?
        super().__init__(*args, **kwds)
        self.cur_step = 1
        self.gif_writer = _gif_writer.GifWriter(
            filename, render, divide, frames, time, scale, gif_options, tmp_dir)

    def set_project(self, project):
        super().set_project(project)
        self.gif_writer.set_project(project)

    def update_colors(self):
        super().update_colors()
        if self.gif_writer.step(self.cur_step):
            self.project.stop()
        else:
            self.cur_step += 1

    def cleanup(self):
        self.gif_writer.write()
