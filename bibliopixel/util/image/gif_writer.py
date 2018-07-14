import os, shutil, tempfile, time, traceback
from . import gif, renderer
from .. import colors, log


DEFAULT_RENDER = {
    'color': colors.Black,
    'pixel_width': 12,
    'pixel_height': None,
    'ellipse': True,
    'vertical': False,
    'frame': 3,
    'padding': 1,
}


class GifWriter:
    """Write an animated GIF given frames from an animation."""

    def __init__(self, filename='gif_writer', render=None,
                 divide=1, frames=128, time=10, scale=1.0, gif_options=None,
                 tmp_dir=None):
        self.render = dict(DEFAULT_RENDER, **(render or {}))
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
        self.times = []

    def set_layout(self, layout):
        self.render = renderer.renderer(layout, **self.render)
        assert self.render

    def step(self, cur_step):
        if self.finished or (self.divide >= 1 and cur_step % self.divide):
            return True

        frame = cur_step / max(self.divide, 1)
        self.times.append(time.time())

        if self.time:
            elapsed = self.times[-1] - self.times[0]
            self.finished = (elapsed >= self.time)
        else:
            self.finished = (frame >= self.frames)

        if self.finished:
            self.write()
            return True

        frame_name = '%s%04d.gif' % (self.basename, frame)
        filename = os.path.join(self.tmp_dir_name, frame_name)

        self.render().save(filename)
        self.frame_files.append(filename)

    def write(self):
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
