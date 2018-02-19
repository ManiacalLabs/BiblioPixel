import math, os, shutil, tempfile, time
from . import collection
from .. util.image import gif, renderer
from .. util import colors, log


DEFAULT_RENDER = {
    'color': colors.Black,
    'pixel_width': 4,
    'pixel_height': None,
    'ellipse': False,
    'vertical': False,
    'frame': 2,
    'padding': 2,
}


class GifWriter(collection.Wrapper):
    """Write animated GIFs for each frame in the contained animation"""

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
        render = dict(DEFAULT_RENDER, **(render or {}))
        self.render = renderer.renderer(self.layout, **render)
        self.divide = divide
        self.frames = frames
        self.time = time
        self.frame_files = []
        self.scale = scale
        self.gif_options = gif_options or {}

        filename = os.path.expanduser(os.path.abspath(filename))
        file_root = filename[:-4] if filename.endswith('.gif') else filename
        self.filename = file_root + '.gif'
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        if tmp_dir:
            self.tmp_dir_name = tmp_dir
            shutil.rmtree(tmp_dir, ignore_errors=True)
            os.makedirs(self.tmp_dir_name, exist_ok=True)
        else:
            self.tmp_dir = tempfile.TemporaryDirectory()
            self.tmp_dir_name = self.tmp_dir.name
        self.basename = os.path.basename(file_root)
        self.finished = False
        self.stop_after_write = True

    def pre_run(self):
        super().pre_run()
        self.times = []

    def step(self, amt=1):
        super().step(amt)
        if self.finished or (self.divide >= 1 and self.cur_step % self.divide):
            return

        frame = self.cur_step / max(self.divide, 1)
        self.times.append(time.time())

        if self.time:
            elapsed = self.times[-1] - self.times[0]
            self.finished = (elapsed >= self.time)
        else:
            self.finished = (frame >= self.frames)

        if self.finished:
            self._write_gif_file()
            self.completed = True
        else:
            frame_name = '%s%04d.gif' % (self.basename, frame)
            filename = os.path.join(self.tmp_dir_name, frame_name)

            self.render().save(filename)
            self.frame_files.append(filename)

    def _write_gif_file(self):
        if not self.frame_files:
            return

        ff, self.frame_files = self.frame_files, []
        go = dict(self.gif_options)

        if 'duration' in go:
            go.pop('fps', None)
            try:
                go['duration'] *= self.scale
            except:
                go['duration'] = [g * self.scale for g in go['duration']]

        elif 'fps' in go:
            go['fps'] /= self.scale

        else:
            # Compute the list of durations from the list of times
            duration = []
            for i, time in enumerate(self.times):  # noqa: 402
                if not i:
                    previous_time = time
                else:
                    # GIFs only accept time in 0.01 second increments
                    duration.append(round(time - previous_time, 2))
                    previous_time += duration[-1]

            duration.append(duration[-1])
            go = dict(go, duration=duration)

        gif.write_animation(self.filename, ff, **go)
        self.tmp_dir = None

    def __del__(self):
        try:
            self._write_gif_file()
        except Exception as e:
            log.error('Failed to write GIF file: %s', e)
